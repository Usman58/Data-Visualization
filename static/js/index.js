
/*
$(document).ready(function () {
  $("#post-form").on("submit", function (event) {
    event.preventDefault();
    $.ajax({
      url: " http://127.0.0.1:8000/summarizecolumns/", // the endpoint
      type: "POST", // http method
      //data : { the_post : $('#post-text').val() }, // data sent with the post request
      data: {
        name: $("#sumselect option:selected").val(),
        db: $("#db").val(),
        table: $("#table").text(),
      },
      // handle a successful response

      success: function (res) {
        $("#summarize").remove();
        result = res.summarizecolumns;
        $("#sumName").append(
          "Summarize by" + "    " + res.summarizecolumns.Name
        );
        $.each(result, function (key, value) {
          console.log(key);
          $("#summarizecoulmns").css("display", "block");
          $("#sumselectcol").append(`<option value="${key}"> ${key} </option>`);
        });
      },
      error: function (xhr, errmsg, err) {
        console.log("error");
      },
    });
  });
});
*/