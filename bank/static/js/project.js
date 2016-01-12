(function(window){
    var $display = $("#display");
    var $key = $(".keyboard li");
    var $form = $("#form_id");
    var $input = $("#input_id");
    var $clear = $(".clear");
    var txt = $display.text();
    var val = "";
    var view = $display.data("view");
    $key.on('click', function(e) {
        var $this = $(this);
        var x = $this.text();
        if (view == "login") {
            if (val.length >= 16) return;
            if (val.length > 0 && val.length % 4 == 0) txt += '-';
            txt += x;
        } else if (view == "pin") {
            if (val.length >= 4) return;
            txt += '*';
        } else if (view == 'withdraw') {
            if (txt.length == 0 && x == '0') return;
            txt += x;
        }
        val += x;
        $display.text(txt);
    });
    $form.on('submit', function(e) {
        e.preventDefault();
        $input.val(val);
        this.submit();
    });
    $clear.on('click', function(e) {
        txt = val = "";
        $display.text(txt);
    });
})(window);
