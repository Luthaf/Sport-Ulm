function update_from_clipper() {
    function status (finish_trigger) {
        function call_myself() {
            status(finish_trigger);
        }

        $.ajax( "update_from_clipper_status", {
            success: function(data, status, jqXHR) {
                if (finish_trigger.finished == false) {
                    $("#update_status span").text(data);
                }
            },
            error: function(data, status, jqXHR) {
                if (finish_trigger.finished == false) {
                    $("#update_status span").text(
                        "Impossible de récupérer l'avancement de la mise à jour…");
                    }
                },
                complete: function(data, status, jqXHR) {
                    if (finish_trigger.finished == false) {
                        setTimeout(call_myself(), 500);
                    }
                }
            });
        }

    function update (finish_trigger) {
        $.ajax( "update_from_clipper", {
            beforeSend: function(jqXHR, settings) {
                setTimeout(status(finish_trigger), 500);
            },
            success: function(data, status, jqXHR) {
                $("#update_status").addClass("btn-success");
                $("#update_status i").addClass("icon-green");
                $("#update_status span").text(" À jour");
            },
            error: function (data, status, jqXHR) {
                $("#update_status").addClass("btn-warning");
                $("#update_status i").addClass("icon-red");
                $("#update_status span").text(" Échec de la mise à jour");
            },
            complete: function(data, status, jqXHR) {
                finish_trigger.finished = true;
            }
        });
    }

    $( "#update_status" ).click(function() {
        var finish_trigger = {finished: false};
        update(finish_trigger);
    });
}

$( update_from_clipper );