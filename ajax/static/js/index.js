$(document).ready(function(){
    $("#search_btn").click(function(){
        var formData = $('#search_bar').val();
 
        //formData = new
        $.ajax({
            type: "POST",
            data: formData,
            success: function(data, textStatus) {
                $("#res").text(data);    
                    },
            error: function() {
                alert('Not OKay');
            }
});​
        
            
        
        
    });
 });