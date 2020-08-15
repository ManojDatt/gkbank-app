$(document).ready(function(){
	$('a:contains("Add Transaction")').text('$ Make Transaction');
	$(document).on('click', '.download_statement', function(e){
		e.preventDefault()
		customers = $('#customers_list').val()
		from_date = $('#from_date').val()
		to_date = $('#to_date').val()
		if(to_date != '' && from_date != '' && customers.length > 0){
			formSubmit(from_date, to_date, customers)
			$('#from_date').val('')
			$('#to_date').val('')
		}else{
			alert('Any of the required data (Customers, From Date & To Date) is not valid.')
		}
	})
	$(document).on('click', '.user_statements, .downloads', function(e){
		e.preventDefault()
		console.log($(this).attr('data-id'))
		var customers =[]
		if(e.currentTarget.classList[2] === 'downloads'){
			customers = $('.action-select').map(function(){ if($(this).is(':checked')) {return  $(this).val()} }).get()
		}else{
			customers = [$(this).attr('data-id')]
		}
		console.log(customers)
		if(customers.length > 0){
			$('#customers_list').val(customers)
			jQuery.noConflict();
			$("#modalScrollable").modal('show')
		}
	})
})

function formSubmit(from_date, to_date, customers){
	var form = document.createElement("form");
	var from = document.createElement("input"); 
	var to = document.createElement("input");
	var customer = document.createElement("input");
	var token = document.createElement("input");
	form.method = "POST";
	form.action = "/extras/download-statement"; 

	from.value=from_date;
	from.name="from";
	form.appendChild(from); 

	to.value=to_date;
	to.name="to";
	form.appendChild(to);

	customer.value = customers
	customer.name= 'customers'
	form.appendChild(customer);

	token.value = $('input[name="csrfmiddlewaretoken"]').val()
	token.name = 'csrfmiddlewaretoken'
	form.appendChild(token);

	document.body.appendChild(form);
	form.submit();
}
$(function(){
	$('#from_date').datetimepicker({
		format:'d/m/Y',
		onShow:function( ct ){
			this.setOptions({
			    maxDate:$('#to_date').val()?$('#to_date').val():false
			})
		},
		timepicker:false
	});
	$('#to_date').datetimepicker({
		format:'d/m/Y',
		onShow:function( ct ){
			this.setOptions({
			    minDate:$('#from_date').val()?$('#from_date').val():false
			})
		},
		timepicker:false
	});
});