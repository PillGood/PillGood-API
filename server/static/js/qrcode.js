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

        $('#submit').on('click', function() {
            request_data = {}
            
            hospital_name = $("#hospital_name").val();
            // if(hospital_name === "") {
            //     alert("의료기관 명칭을 입력해주세요.");
            //     return;
            // }
            request_data['hospital_name'] = hospital_name;

            hospital_tel = $("#hospital_tel").val();
            // if(hospital_tel === "") {
            //     alert("의료기관 연락처를 입력해주세요.");
            //     return;
            // }
            request_data['hospital_tel'] = hospital_tel;

            user_name = $("#user_name").val();
            // if(user_name === "") {
            //     alert("환자 이름을 입력해주세요.");
            //     return;
            // }
            request_data['user_name'] = user_name;

            user_id = $("#user_id").val();
            // if(user_id === "") {
            //     alert("환자 주민등록번호를 입력해주세요.");
            //     return;
            // }
            request_data['user_id'] = user_id;
            
            request_data['pills'] = [];
            $(".collection-item").each(function(index) {
                if(index < 2) {
                    return;
                }

                pill_name = $(this).find('#pill_name').text().trim();
                one_dose = $(this).find('#one_dose').text().trim();
                day_dose = $(this).find('#day_dose').text().trim();
                dose_days = $(this).find('#dose_days').text().trim();
                dose_time = $(this).find('#dose_time').text().trim();

                request_data['pills'].push({
                    'pill_name': pill_name,
                    'one_dose': one_dose,
                    'day_dose': day_dose,
                    'dose_days': dose_days,
                    'dose_time': dose_time
                });
            });

            $.ajax({
                type: "POST",
                url: '/qrcode',
                data: request_data,
                contentType: "application/json",
                success: function(data) {
                    console.log(data);
                    $('#qrcode').attr('src', data.url);
                    $('#modal2').modal('open');
                }
              });

        });
    });
  })(jQuery);
  