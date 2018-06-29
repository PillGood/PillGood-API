(function($){
    $(function(){
        $('#save_pill').on('click', function() {
            var modal = $("#modal1");
            var pill_name = modal.find("#pill_name").val();
            if(pill_name === "") {
                alert("처방 의약품 명칭을 입력하세요.")
                return;
            }

            var one_dose = modal.find("#one_dose").val();
            if(one_dose === "") {
                alert("1회 투여량을 입력하세요.")
                return;
            }
            var day_dose = modal.find("#day_dose").val();
            if(day_dose === "") {
                alert("1일 투여횟수를 입력하세요.")
                return;
            }
            
            var dose_days = modal.find("#dose_days").val();
            if(dose_days === "") {
                alert("투약 일수를 입력하세요.")
                return;
            }
            
            var dose_time = modal.find("#dose_time").val();

            // 새 리스트 생성
            var pill_item = $("#pill-template").clone();
            pill_item.show();
            pill_item.find("#pill_name").text(pill_name);
            pill_item.find("#one_dose").text(one_dose);
            pill_item.find("#day_dose").text(day_dose);
            pill_item.find("#dose_days").text(dose_days);
            pill_item.find("#dose_time").text(dose_time);

            // 추가
            $(".collection").append(pill_item);
        });
    });
  })(jQuery);
  