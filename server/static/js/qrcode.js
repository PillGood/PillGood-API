(function($){
    $(function(){
        // ㅎ_ㅎ
        $("#hospital_name").val('오픈핵 병원');
        $("#date").val('20180630');
        $("#user_name").val('약쟁이');
        $("#user_id").val('980101-XXXXXXX');

        $('#save_pill').on('click', function() {
            var modal = $("#modal1");

            var pill_id = modal.find("#pill_id").val();
            if(pill_id === "") {
                alert("의약품 번호를 입력하세요.")
                return;
            }

            var pill_name = modal.find("#pill_name").val();
            if(pill_name === "") {
                alert("의약품 명칭을 입력하세요.")
                return;
            }
            
            var dose_time = modal.find("#dose_time").val();

            // 새 리스트 생성
            var pill_item = $("#pill-template").clone();
            pill_item.show();
            pill_item.find("#pill_id").text(pill_id);
            pill_item.find("#pill_name").text(pill_name);
            pill_item.find("#dose_time").text(dose_time);

            // 추가
            $(".collection").append(pill_item);
        });

        $('#submit').on('click', function() {
            request_data = {}
            
            hospital_name = $("#hospital_name").val();
            if(hospital_name === "") {
                alert("의료기관 명칭을 입력해주세요.");
                return;
            }
            request_data['hospital_name'] = hospital_name;

            date = $("#date").val();
            if(date === "") {
                alert("처방 일을 입력해주세요.");
                return;
            }
            request_data['date'] = date;

            user_name = $("#user_name").val();
            if(user_name === "") {
                alert("환자 이름을 입력해주세요.");
                return;
            }

            request_data['user_name'] = user_name;

            user_id = $("#user_id").val();
            request_data['user_id'] = user_id;
            
            request_data['pills'] = [];
            $(".collection-item").each(function(index) {
                if(index < 2) {
                    return;
                }

                pill_id = $(this).find("#pill_id").text().trim();
                pill_name = $(this).find('#pill_name').text().trim();
                dose_time = $(this).find('#dose_time').text().trim();

                request_data['pills'].push({
                    'pill_id': pill_id,
                    'pill_name': pill_name,
                    'dose_time': dose_time
                });
            });

            $.ajax({
                type: "POST",
                url: '/qrcode',
                data: JSON.stringify(request_data),
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
  