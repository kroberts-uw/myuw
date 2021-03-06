var TuitionCard = {
    name: 'TuitionCard',
    dom_target: undefined,

    render_init: function() {
        if (!window.user.student) {
            $("#TuitionCard").hide();
            return;
        }
        WSData.fetch_tuition_data(TuitionCard.render_upon_data,
                                  TuitionCard.render_error);
        WSData.fetch_notice_data(TuitionCard.render_upon_data,
                                 TuitionCard.render_error);
    },

    _has_all_data: function () {
        if (WSData.tuition_data() && WSData.notice_data()) {
            return true;
        }
        return false;
    },

    render_error: function (status) {
        // notice never returns 404.
        if (status === 404) {
            // not student or SDB can't find the regid
            TuitionCard.dom_target.hide();
            return;
        }
        var raw = CardWithError.render("Tuition & Fees");
        TuitionCard.dom_target.html(raw);
    },

    render_upon_data: function() {
        // Having multiple callbacks come to this function,
        // delay rendering until all requests are complete.
        if (!TuitionCard._has_all_data()) {
            return;
        }

        // _render should be called only once.
        if (renderedCardOnce(TuitionCard.name)) {
            return;
        }
        TuitionCard._render();
    },

    process_tuition: function(data) {
        var is_credit = false;
        if (data.match(" CR")) {
            is_credit = true;
            data = data.replace(" CR", "");
        }
        return {
            tuition: data,
            is_credit: is_credit
        };
    },

    _render: function () {
        var template_data = WSData.tuition_data(),
            tuition_due_notice,
            display_date,
            due_date,
            has_credit_values;

        template_data.pce_tuition_dup = Notices.get_notices_for_tag("pce_tuition_dup");
        template_data.is_pce = false;

        if (template_data.pce_accbalance == '0.00') {
            template_data.pce_accbalance = 0;
        }

        has_credit_values = TuitionCard.process_tuition(template_data.tuition_accbalance);
        template_data.plain_tuition = has_credit_values.tuition;
        template_data.is_credit = has_credit_values.is_credit;

        tuition_due_notice = Notices.get_notices_for_tag("tuition_due_date")[0];
        if (tuition_due_notice !== undefined) {
            for (var i = 0; i < tuition_due_notice.attributes.length; i += 1) {
                if (tuition_due_notice.attributes[i].name === "Date") {
                    due_date = new Date(tuition_due_notice.attributes[i].value.replace(/-/g, "/"));
                    display_date = tuition_due_notice.attributes[i].formatted_value;
                }
            }
        }
        if (due_date !== undefined) {
            template_data.tuition_date = display_date;
            template_data.tuition_date_offset = TuitionCard._days_from_today(due_date);

            //Alert banners
            if(parseFloat(template_data.tuition_accbalance) > 0){
                if(template_data.tuition_date_offset === 0){
                    template_data.due_today = true;
                }
                if (template_data.tuition_date_offset < 0){
                    template_data.past_due = true;
                }
            }
        }
        template_data.has_balance = parseInt(template_data.tuition_accbalance) > 0;
        var finaid_tags = ["tuition_aidhold_title",
                           "tuition_missingdocs_title",
                           "tuition_loanpromissory_title",
                           "tuition_loancounseling_title",
                           "tuition_acceptreject_title",
                           "tuition_disbursedateA_title",
                           "tuition_disbursedateB_title",
                           "tuition_direct_deposit_title",
                           "tuition_aid_prioritydate_title",
                           "tuition_aid_reminder_title",
                           "tuition_summeraid_date_title",
                           "tuition_summeraid_avail_title"
                          ];
        template_data.finaid_notices = Notices.get_ordered_finaid_notices(finaid_tags);
        var source = $("#tuition_card").html();
        var template = Handlebars.compile(source);
        TuitionCard.dom_target.html(template(template_data));
        LogUtils.cardLoaded(TuitionCard.name, TuitionCard.dom_target);
        TuitionCard._init_events();
    },

    _days_from_today: function (date) {
        var today = new Date();
        return Math.ceil((date - today) / (1000*60*60*24));
    },

    _init_events: function(){
        $(".finaid-panel-default").find('a').each(function(idx, elm){
            $(elm).on('click', function(e){
                var content = $(e.target).parents('li').find('.finaid-panel-collapse');
                if(content.attr('aria-hidden')){
                    content.attr('aria-hidden', false);
                } else{
                    content.attr('aria-hidden', true);
                }
            });
        });
    }
};

/* node.js exports */
if (typeof exports == "undefined") {
    var exports = {};
}
exports.TuitionCard = TuitionCard;
