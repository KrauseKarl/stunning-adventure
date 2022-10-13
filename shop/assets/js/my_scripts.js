// АВТОЗАПОЛЕНИЕ ПОЛЕ ЗАКАЗА
//document.querySelector('#step_4').addEventListener('click', function () {
//        var name = document.getElementById('name').value
//        var telephone = document.getElementById('telephone').value
//        var email = document.getElementById('email').value
//        var delivery_or = document.getElementById('delivery_or').innerText;
//        var city = document.getElementById('city').value
//        var address = document.getElementById('address').value
//        var pay_my = document.getElementById('pay_my').innerText;
//
//        document.getElementById('name_result').innerHTML = name
//        document.getElementById('telephone_result').innerHTML =  telephone
//        document.getElementById('email_result').innerHTML =  email
//        document.getElementById('pay_result').innerHTML =  pay_my
//        document.getElementById('delivery_result').innerHTML = delivery_or
//        document.getElementById('city_result').innerHTML =  city
//        document.getElementById('address_result').innerHTML =  address
//        document.getElementById('pay_result').innerHTML =  pay_my
//
//        localStorage.removeItem('order');
//        }
//    )

$(".Comment:gt(0)").hide();
$("#hide_comment").css('display','none')
var comm = $(".Comment")
if(comm.length < 2) {
    $("#show_comment").css('display','none')
}

$('#hide_comment').on('click', function() {
    $(".Comment:gt(0)").hide();
        $("#hide_comment").css('display','none')
        $("#show_comment").css('display','block')
    }
);
$("#show_comment").on('click', function() {
    var comm = $(".Comment")
    $(".Comment").show()
    $("#show_comment").css('display','none')
    $("#hide_comment").css('display','block')

  }
);





//// Модальное окно
//
//// открыть по кнопке
//$('.js-button-campaign').click(function() {
//
//	$('.js-overlay-campaign').fadeIn();
//	$('.js-overlay-campaign').addClass('disabled');
//});
//
//// закрыть на крестик
//$('.js-close-campaign').click(function() {
//	$('.js-overlay-campaign').fadeOut();
//
//});
//
//// закрыть по клику вне окна
//$(document).mouseup(function (e) {
//	var popup = $('.js-popup-campaign');
//	if (e.target!=popup[0]&&popup.has(e.target).length === 0){
//		$('.js-overlay-campaign').fadeOut();
//
//	}
//});
//
//// открыть по таймеру
//$(window).on('load', function () {
//	setTimeout(function(){
//		if($('.js-overlay-campaign').hasClass('disabled')) {
//			return false;
//		} else {
//
//			$(".js-overlay-campaign").fadeIn();
//		}
//	}, 5000);
//});
//

//
//$(document).ready(function(){
//
//    //hide message_body after the first one
//    $(".message_list .message_body:gt(0)").hide();
//
//    //hide message li after the 5th
//    $(".message_list li:gt(4)").hide();
//
//    //toggle message_body
//    $(".message_head").click(function(){
//        $(this).next(".message_body").slideToggle(500)
//        return false;
//    });
//
//    //collapse all messages
//    $(".collpase_all_message").click(function(){
//        $(".message_body").slideUp(500)
//        return false;
//    });
//
//    //show all messages
//    $(".show_all_message").click(function(){
//        $(this).hide()
//        $(".show_recent_only").show()
//        $(".message_list li:gt(4)").slideDown()
//        return false;
//    });
//
//    //show recent messages only
//    $(".show_recent_only").click(function(){
//        $(this).hide()
//        $(".show_all_message").show()
//        $(".message_list li:gt(4)").slideUp()
//        return false;
//    });
//
//});
//if(!localStorage.getItem('order')) {
//    localStorage.setItem('order', JSON.stringify([]))
//}



//(function ($){
//my_order().init();
//document.querySelector('#step_1').addEventListener('click', function(e) {
//        let name = document.getElementById('name').value
//        let telephone = document.getElementById('telephone').value
//        let email = +document.getElementById('email').value
//        if(name && telephone && email) {
//            document.getElementById('name').value = ''
//            document.getElementById('telephone').value = ''
//            document.getElementById('email').value = ''
//            let order = JSON.parse(localStorage.getItem('order'))
//            goods.push(['order_'+order.length, name, telephone, email, 0, 0, 0])
//            localStorage.setItem('order', JSON.stringify(goods))
////            update_goods()
////            myModal.hide()
//        }
//        }
//})
//})(jQuery);