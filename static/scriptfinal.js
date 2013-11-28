function validatestring(){
var shorturl = $("#shorturl").val();

var i,charCode;

for(i=0;i<shorturl.length;i++)
{

	charCode = shorturl.charCodeAt(i);
	if (charCode < 65 || charCode > 122) 
            return false;
}
return true;
}


function canceloperation(e)
{
	e.preventDefault();
}


$(document).ready(function(){


$('button').click(function(){

	var $currbutton = $(this);
	var buttonclass = $currbutton.attr('class');

	if(buttonclass == 'close')
	{
		$(".close").parent().remove();
	}


});



$('form').submit(function(e){

	var $currform = $(this);
	var formname = $currform.attr('id');

if(formname == 'urlform')
{
	if(validatestring())
  {
  		

  		//alert("submitted");
  }
  else
  {	
  		$('#shorturl').parent().parent().attr('class','control-group error')
  		$('#shorturl').parent().append('<span class="help-inline">Please enter alphabets only for the shorturl</span>');
  		canceloperation(e);


  }
}  

if(formname == 'searchform')
{
	if($('#searchip') == '')
	{
		canceloperation(e);
	}
	else
	{
		alert('redirecting');
	}

}

});




  

});





    
    

    
  


