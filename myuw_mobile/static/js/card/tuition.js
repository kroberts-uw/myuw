var TuitionCard = {
    render: function (fina_notices) {
        var source = $("#tuition_card").html();
        var template = Handlebars.compile(source);
        return template();
    },

};
