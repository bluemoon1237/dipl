function setUp(questionCount) {
    $("#main-nav").hide();

    // Set up ajax csrf
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }

            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });

    $('#questionPages').twbsPagination({
        totalPages: questionCount,
        visiblePages: 50,
        onPageClick: function (event, question) {
            submitAnswers(question)
        }
    })
}

function submitAnswers(newQuestion){
    var answers = [];
    $.each($("input[name='answer']:checked"), function() {
        answers.push($(this).val())
    });
    sendAnswers(answers, newQuestion)
}

function sendAnswers(answers, newQuestion) {

    var question_id = $("input[name='question_id']").val();
    var attempt_id = $("input[name='attempt_id']").val();

    activateLoader();

    var data_to_send = {
        question_id: question_id,
        attempt_id: attempt_id,
        answers: answers,
        newQuestion: newQuestion
    };

    console.log(data_to_send);

    $.post({
        url:'/attempt/answers',
        data: data_to_send,
        success: function (data) {
            switch(data.status){
                case 1:
                    $('#questionAnswersDiv').removeClass('loader');
                    $('#questionDiv').html(data.data);
                    break;
                case 2:
                    window.location.replace(data.url);
                    break;
            }
            console.log(data);
        }
    })
}

function activateLoader(){
    $('#questionAnswersDiv').html("").addClass('loader');
}

function onFinishClick(){
    submitAnswers(-1);
    var attempt_id = $("input[name='attempt_id']").val();
    window.location.replace('/attempt/finish/' + attempt_id)
}
