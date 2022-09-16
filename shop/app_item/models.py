from datetime import datetime

from django.contrib.sessions.models import Session
from django.db import models
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.views import View


class ItemView(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE, related_name='views')
    ip = models.CharField(max_length=40)
    session = models.CharField(max_length=40)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'app_views'
        ordering = ['created']


class AvailableManager(models.Manager):
    def get_query_set(self):
        return super().get_query_set().filter(is_available=True)


class UnavailableManager(models.Manager):
    def get_query_set(self):
        return super().get_query_set().filter(is_available=False)


class Item(models.Model):
    title = models.CharField(max_length=100, db_index=True, verbose_name='название')
    slug = models.SlugField(max_length=100, db_index=True, allow_unicode=True)
    description = models.TextField(null=True, blank=True, verbose_name='описание')
    stock = models.PositiveIntegerField(verbose_name='количество')
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='цена')
    is_available = models.BooleanField(default=False, verbose_name='в наличии')
    limited_edition = models.BooleanField(default=False, verbose_name='ограниченный тираж')
    reviews = models.SmallIntegerField(default=0, verbose_name='просмотры')
    comments = models.SmallIntegerField(default=0, verbose_name='комментарии')
    created = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    updated = models.DateTimeField(auto_now_add=True, verbose_name='дата обновления')

    image = models.ImageField(upload_to='item/%Y/%m/%d', null=True, blank=True, verbose_name='изображение')

    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, related_name='items',
                                 verbose_name='категория')
    tag = models.ManyToManyField('Tag', max_length=20, blank=True, related_name='item_tags', verbose_name='тег')

    objects = models.Manager()
    available_items = AvailableManager()
    unavailable_items = UnavailableManager()

    class Meta:
        db_table = 'app_items'
        ordering = ['created']
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Функция по созданию slug"""
        if not self.slug:
            self.slug = slugify(self.title)
        super(Item, self).save(*args, **kwargs)

    def record_view(self, request, item_id):
        """Функция увеличивает  количество просмотров при посещении страницы товара"""
        item = get_object_or_404(Item, pk=item_id)
        if request.user.is_authenticated:
            if not ItemView.objects.filter(
                    item=item,
                    session=request.session.session_key):
                view = ItemView.objects.create(
                    item=item,
                    ip=request.META['REMOTE_ADDR'],
                    created=datetime.now(),
                    session=request.session.session_key
                )
                view.save()
        else:
            if not ItemView.objects.filter(
                    item=item,
                    ip=request.META['REMOTE_ADDR']):
                view = ItemView.objects.create(
                    item=item,
                    ip=request.META['REMOTE_ADDR'],
                    created=datetime.now(),
                    session=''
                )
                view.save()
        return ItemView.objects.filter(item=item).count()


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='название')
    slug = models.SlugField(max_length=100, db_index=True, allow_unicode=True)
    description = models.TextField(null=True, blank=True, verbose_name='описание')
    image = models.ImageField(upload_to='category', null=True, verbose_name='иконка')
    parent_category = models.ForeignKey('self', related_name='sub_categories',
                                        on_delete=models.SET_NULL, null=True, blank=True)
    item = models.ForeignKey('Item', on_delete=models.CASCADE, related_name='cats')

    objects = models.Manager()

    class Meta:
        db_table = 'app_categories'
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)


class Tag(models.Model):
    title = models.CharField(max_length=50, unique=True, blank=True, verbose_name='название тега')
    slug = models.SlugField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True, verbose_name='активный')

    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'app_tags'
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def save(self, *args, **kwargs):
        """Функция по созданию slug"""
        if not self.slug:
            self.slug = slugify(self.title)
        super(Tag, self).save(*args, **kwargs)


class Comment(models.Model):
    review = models.TextField(verbose_name='комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='дата обновления')
    is_published = models.BooleanField(default=False, verbose_name='опубликовано')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='item_comments', verbose_name='товар')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments', verbose_name='пользователь')

    # session = models.ForeignKey(Session, on_delete=models.SET_NULL, blank=True, null=True)
    objects = models.Manager()

    def __str__(self):
        return self.review[:15]

    class Meta:
        db_table = 'app_comments'
        ordering = ['-created_at']
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'


class Image(models.Model):
    title = models.CharField(max_length=200, null=True, verbose_name='название')
    created = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    updated = models.DateTimeField(auto_now_add=True, verbose_name='дата изменения')
    main_image = models.BooleanField(default=False, verbose_name='главное изображения')
    image = models.ImageField(upload_to='gallery/%Y/%m/%d', default='static/img/default_flat.jpg', null=True,
                              blank=True, verbose_name='изображение')
    objects = models.Manager()

    class Meta:
        db_table = 'app_images'
        ordering = ['title']
        verbose_name = 'изображение'
        verbose_name_plural = 'изображения'

    def __str__(self):
        return self.title

#
# class Cart(models.Model):
#
#     user = models.OneToOneField(User, blank=True, null=True, related_name='cart', on_delete=models.CASCADE)
#     owner = models.ForeignKey('Customer', null=True, verbose_name='Владелец', on_delete=models.CASCADE)
#     products = models.ManyToManyField('CartProduct', blank=True, related_name='related_cart')
#     total_products = models.PositiveIntegerField(default=0)
#     final_price = models.DecimalField(max_digits=10, default=0, decimal_places=2, verbose_name='Общая сумма')
#     in_order = models.BooleanField(default=False)
#     for_anonymoys_user = models.BooleanField(default=False)
#     session_key = models.CharField(max_length=40, null=True, blank=True)
#
#     class Meta:
#         verbose_name = 'Корзина'
#         verbose_name_plural = 'Корзина'
#         unique_together = ('user', 'session_key',)
#
#     def __str__(self):
#         return str(self.id)
#
#
# class CartProduct(models.Model):
#     class Meta:
#         verbose_name = 'Продукт для корзины'
#         verbose_name_plural = 'Продукты для корзины'
#
#     user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
#     cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
#     # #########################################&&&&&&&&&&?????????????????????????????
#     product = models.ForeignKey('Product', verbose_name='Товар', on_delete=models.CASCADE)
#     qty = models.PositiveIntegerField(default=1)
#     final_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая сумма')
#
#     def __str__(self):
#         return "Продукт: {} (для корзины)".format(self.product.title)
#
#     def save(self, *args, **kwargs):
#         self.final_price = self.qty * self.product.price
#         super().save(*args, **kwargs)
#
#
# class Customer(models.Model):
#     class Meta:
#         verbose_name = 'Покупатель'
#         verbose_name_plural = 'Покупатели'
#
#     user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
#     phone = models.CharField(max_length=20, verbose_name='Номер телефона')
#     adress = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)
#     orders = models.ManyToManyField('Order', verbose_name='Заказы покупателя', related_name='related_order')
#
#     def __str__(self):
#         return "Покупатель: {} {}".format(self.user.first_name, self.user.last_name)
#
#
# class Order(models.Model):
#     class Meta:
#         verbose_name = 'Заказ'
#         verbose_name_plural = 'Заказы'
#
#     STATUS_NEW = 'new'
#     STATUS_IN_PROGRESS = 'in_progress'
#     STATUS_READY = 'is_ready'
#     STATUS_COMPLETED = 'completed'
#     STATUS_DEACTIVE = 'deactive'
#
#     BUYING_TYPE_SELF = 'self'
#     BUYING_TYPE_DELIVERY = 'delivery'
#
#     STATUS_CHOICES = (
#         (STATUS_NEW, 'Новый заказ'),
#         (STATUS_IN_PROGRESS, 'Заказ в обработке'),
#         (STATUS_READY, 'Заказ готов'),
#         (STATUS_COMPLETED, 'Заказ выполнен'),
#         (STATUS_DEACTIVE, 'Заказ Отменен')
#     )
#
#     BUYING_TYPE_CHOICES = (
#         (BUYING_TYPE_SELF, 'Самовывоз'),
#         (BUYING_TYPE_DELIVERY, 'Доставка')
#     )
#
#     customer = models.ForeignKey(Customer, verbose_name='Покупатель', related_name='related_orders',
#                                  on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=255, verbose_name='Имя')
#     last_name = models.CharField(max_length=255, verbose_name='Фамилия')
#     phone = models.CharField(max_length=20, verbose_name='Телефон')
#     cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE, null=True, blank=True)
#     adress = models.CharField(max_length=1024, verbose_name='Адрес', null=True, blank=True)
#     otdel = models.CharField(max_length=20, verbose_name='Отделение', null=True, blank=True)
#     status = models.CharField(
#         max_length=100,
#         verbose_name='Статус заказ',
#         choices=STATUS_CHOICES,
#         default=STATUS_NEW
#     )
#     buying_type = models.CharField(
#         max_length=100,
#         verbose_name='Тип заказа',
#         choices=BUYING_TYPE_CHOICES,
#         default=BUYING_TYPE_SELF
#     )
#     comment = models.TextField(verbose_name='Комментарий к заказу', null=True, blank=True)
#     created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания заказа')
#     order_date = models.DateField(verbose_name='Дата получения заказа', default=timezone.now)
#
#     def __str__(self):
#         return str(self.id)
#
#
# class Rewiews(models.Model):
#     name = models.CharField(max_length=255, verbose_name='Имя')
#     text = models.TextField('Сообщение', max_length=500)
#     parent = models.ForeignKey(
#         'self', verbose_name='Родитель', on_delete=models.SET_NULL, blank=True, null=True
#     )
#     product = models.ForeignKey('Product', verbose_name='Продукт', on_delete=models.CASCADE)
#     data = models.DateTimeField(auto_now=True, db_index=True, verbose_name='Добавлено')
#
#     def __str__(self):
#         return f"{self.name}-{self.product}"
#
#     class Meta:
#         verbose_name = 'Отзыв'
#         verbose_name_plural = 'Отзывы'
#
#
# class CartMixin(View):
#     def dispatch(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             customer = Customer.objects.filter(user=request.user).first()
#             if not customer:
#                 customer = Customer.objects.create(
#                     user=request.user
#                 )
#             cart = Cart.objects.filter(owner=customer, in_order=False).first()
#             if not cart:
#                 cart = Cart.objects.create(owner=customer)
#         else:
#             cart = Cart.objects.filter(for_anonymoys_user=True).first()
#             if not cart:
#                 cart = Cart.objects.create(for_anonymoys_user=True)
#         self.cart = cart
#         self.cart.save()
#         return super().dispatch(request, *args, **kwargs)
#
#
# class AddToCartView(CartMixin, View):
#     def get(self, request, *args, **kwargs):
#         product_slug = kwargs.get('slug')
#         product = Product.objects.get(slug=product_slug)
#
#         if request.user.is_authenticated:
#             cart_product, created = CartProduct.objects.get_or_create(
#                 user=self.cart.owner, cart=self.cart, product=product
#             )
#             if created:
#                 self.cart.products.add(cart_product)
#             recalc_cart(self.cart)
#             messages.add_message(request, messages.INFO, 'Товар добавлен в корзину')
#             return redirect(product.get_absolute_url())
#         else:
#             # print(request.session['cartanon'])
#             cart, created = Cart.objects.get_or_create(
#                 session_key=request.session.session_key,
#                 defaults={'user': None}
#             )
#             return redirect(product.get_absolute_url())
#             # except:
#             #     new_cart = Cart()
#             # new_cart.save()
#             # request.session["cart_id"] = new_cart.id
#             # new_cart.products.add(product)
#             # new_cart.save()
#             # return HttpResponse("<h1>okkk!</h1>")
#
#
# class DeleteFomCartView(CartMixin, View):
#
#     def get(self, request, *args, **kwargs):
#         product_slug = kwargs.get('slug')
#         product = Product.objects.get(slug=product_slug)
#         cart_product = CartProduct.objects.get(
#             user=self.cart.owner, cart=self.cart, product=product
#         )
#         self.cart.products.remove(cart_product)
#         cart_product.delete()
#         recalc_cart(self.cart)
#         messages.add_message(request, messages.INFO, 'Товар Удален')
#         return HttpResponseRedirect('/cart/')
#
#
# class ChangeQTYView(CartMixin, View):
#     def post(self, request, *args, **kwargs):
#
#         product_slug = kwargs.get('slug')
#         product = Product.objects.get(slug=product_slug)
#         cart_product = CartProduct.objects.get(
#             user=self.cart.owner, cart=self.cart, product=product
#         )
#         if request.POST.get('qty') == '1':
#             cart_product.qty += 1
#             cart_product.save()
#             recalc_cart(self.cart)
#         if request.POST.get('qty') == '0':
#             cart_product.qty -= 1
#             cart_product.save()
#             recalc_cart(self.cart)
#
#         messages.add_message(request, messages.INFO, 'Кол-во изменено')
#         return HttpResponseRedirect('/cart/')
#
#
# class CartView(CartMixin, View):
#
#     def get(self, request, *args, **kwargs):
#         category = Category.objects.all()
#         context = {
#             'cart': self.cart,
#             'category': category
#         }
#         return render(request, 'cart.html', context)
#
#
# class CheckoutView(CartMixin, View):
#
#     def get(self, request, *args, **kwargs):
#         category = Category.objects.all()
#         form = OrderForm(request.POST or None)
#         context = {
#             'cart': self.cart,
#             'category': category,
#             'form': form
#         }
#         return render(request, 'checkout.html', context)
#
#
# class MakeOrderView(CartMixin, View):
#
#     def post(self, request, *args, **kwargs):
#         form = OrderForm(request.POST or None)
#         customer = Customer.objects.get(user=request.user)
#         if form.is_valid():
#             new_order = form.save(commit=False)
#             new_order.customer = customer
#             new_order.phone = form.cleaned_data['phone']
#
#             phone = form.cleaned_data['phone']
#
#             new_order.first_name = form.cleaned_data['first_name']
#
#             name = form.cleaned_data['first_name']
#
#             new_order.last_name = form.cleaned_data['last_name']
#             new_order.adress = form.cleaned_data['adress']
#
#             email = form.cleaned_data['adress']
#
#             new_order.otdel = form.cleaned_data['otdel']
#             new_order.buying_type = form.cleaned_data['buying_type']
#             new_order.order_date = form.cleaned_data['order_date']
#             new_order.comment = form.cleaned_data['comment']
#
#             comment = form.cleaned_data['comment']
#
#             new_order.save()
#             self.cart.in_order = True
#             self.cart.save()
#             new_order.cart = self.cart
#             new_order.save()
#             customer.orders.add(new_order)
#
#             # email=form.cleaned_data['adress']
#             # print(email)
#             # name= form.cleaned_data['first_name']
#             # body= form.cleaned_data['phone']
#             send_email(email, name, phone, comment)
#
#             messages.add_message(request, messages.INFO, 'Спасибо за заказ! Менеджер с Вами свяжется')
#             return HttpResponseRedirect('/')
#         return HttpResponseRedirect('/checkout/')
