$(function () {
    $('#mad_residence_uninsured_loss__row').after('<tr><td class="w2p_fw">% of Total Uninsured Loss / Fair Market Value</td><td id="pct-tul"></td></tr>');
    $('#mad_residence_uninsured_loss, #mad_residence_estpredistfmv').change(function (evt) {
        var fmv, pct, ul;
        fmv = Number($('#mad_residence_estpredistfmv').val());
        ul = Number($('#mad_residence_uninsured_loss').val());
        pct = ul / fmv * 100;
        if (!isNaN(pct) && isFinite(pct) && pct != 0) {
            $('#pct-tul').text(String(pct) + '%');
        }
    });
});
