(function () {

    const btnEliminacion = document.querySelectorAll(".btnEliminacion");
    btnEliminacion.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const confirmacion = confirm('¿Seguro de eliminar el producto?');
            if (!confirmacion) {
                e.preventDefault();
            }
        });
    });
})();



(document).ready(function(){
    (".subscription-button").click(function(e){
        e.preventDefault();
        var price = $(this).data('price');
        var subscriptionType = $(this).data('subscription-type');
        $("#amount-input").val(price);
        $("#subscription-type-input").val(subscriptionType);
        $("#subscription-form").submit();
    });
});