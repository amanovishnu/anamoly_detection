$("body")

    .on("click", "#submit-form", function (event) {
        let new_data = {
            src_bytes: parseFloat($("#src_bytes").val()),
            dst_bytes: parseFloat($("#dst_bytes").val()),
            dst_host_srv_count: parseFloat($("#dst_host_srv_count").val()),
            FLAG_SF: $("#flag_sf").val() === "True",
            dst_host_diff_srv_rate: parseFloat($("#dst_host_diff_srv_rate").val()),
            dst_host_rerror_rate: parseFloat($("#dst_host_rerror_rate").val()),
            diff_srv_rate: parseFloat($("#diff_srv_rate").val()),
            count: parseFloat($("#count").val()),
            rerror_rate: parseFloat($("#rerror_rate").val()),
            dst_host_serror_rate: parseFloat($("#dst_host_serror_rate").val())
        };

        $.ajax({
            url: "/predict_anomaly",
            type: 'POST',
            data: JSON.stringify(new_data),
            contentType: "application/json",
            success: function (result, textStatus, xhr) {
                if (result["output"] == 1)
                    $("#output-div").text("ANOMALY")
                else
                    $("#output-div").text("NOT ANOMALY")

                $("#loading-div").addClass("d-none");
                $("#result-div").removeClass("d-none");

                setTimeout(function () {
                    $("input[type='number']").val("");
                    $("#result-div").fadeOut("slow", function () {
                        $(this).addClass("d-none");
                        $("#loading-div").fadeIn("slow", function () {
                            $(this).removeClass("d-none");
                        });
                    });
                }, 5000);
            }
        });
    })