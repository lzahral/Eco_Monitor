(function ($) {

    'use strict';
	
    // ------------------------------------------------------- //
    // Countdown
    // ------------------------------------------------------ //
    $('#countdown').countdown('2019/12/24', function(event) {
	    var $this = $(this).html(event.strftime(''
			+ '<div class="counter"><span>%D</span><p>روز</p></div>'
			+ '<div class="counter"><span>%H</span><p>ساعت</p></div>'
			+ '<div class="counter"><span>%M</span><p>دقیقه</p></div>'
			+ '<div class="counter"><span>%S</span><p>ثانیه</p></div>'
		));
	});

})(jQuery);