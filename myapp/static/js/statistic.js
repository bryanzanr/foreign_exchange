$(document).ready(function(){
  var today = new Date();
  var mm = today.getMonth()+1; //January is 0!
  var year = today.getFullYear();
  var label = [];
  var dat = [];
  var table = $("#table_id").DataTable();
  var data = table.columns().data();
  var i, Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Des;
  var Jan = 0;
  var Feb = 0;
  var Mar = 0;
  var Apr = 0;
  var May = 0;
  var Jun = 0;
  var Jul = 0;
  var Aug = 0;
  var Sep = 0;
  var Oct = 0;
  var Nov = 0;
  var Des = 0;
  for(i in data[2]){
    var txt = data[2][i];
    var split = txt.split(" ");
    var date = split[0];
    var split = date.split("-");
    var month = split[1];
    switch(month){
      case '01':
        Jan += 1;
        break;
      case '02':
        Feb += 1;
        break;
      case '03':
        Mar += 1;
        break;
      case '04':
        Apr += 1;
        break;
      case '05':
        May += 1;
        break;
      case '06':
        Jun += 1;
        break;
      case '07':
        Jul += 1;
        break;
      case '08':
        Aug += 1;
        break;
      case '09':
        Sep += 1;
        break;
      case '10':
        Oct += 1;
        break;
      case '11':
        Nov += 1;
        break;
      case '12':
        Des += 1;
        break;
    }
  }
  if(mm == '1'){
    label.push('Jan');
    dat.push(Jan);
  } else if(mm == '2'){
    label.push('Jan','Feb');
    dat.push(Jan,Feb);
  } else if(mm == '3'){
    label.push('Jan','Feb','Mar');
    dat.push(Jan,Feb,Mar);
  } else if(mm == '4'){
    label.push('Jan','Feb','Mar','Apr');
    dat.push(Jan,Feb,Mar,Apr);
  } else if(mm == '5'){
    label.push('Jan','Feb','Mar','Apr','May');
    dat.push(Jan,Feb,Mar,Apr,May);
  } else if(mm == '6'){
    label.push('Jan','Feb','Mar','Apr','May','Jun');
    dat.push(Jan,Feb,Mar,Apr,May,Jun);
  } else if(mm == '7'){
    label.push('Jan','Feb','Mar','Apr','May','Jun','Jul');
    dat.push(Jan,Feb,Mar,Apr,May,Jun,Jul);
  } else if(mm == '8'){
    label.push('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug');
    dat.push(Jan,Feb,Mar,Apr,May,Jun,Jul,Aug);
  } else if(mm == '9'){
    label.push('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep');
    dat.push(Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep);
  } else if(mm == '10'){
    label.push('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct');
    dat.push(Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct);
  } else if(mm == '11'){
    label.push('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov');
    dat.push(Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov);
  } else{
    label.push('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Des');
    dat.push(Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Des);
  }
  // window.onload = function() {
  var ctx = $("#myChart");
  var lineChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: label,
      datasets: [{
        label: year,
        data: dat
      }]
    }
  });
  // }
});
// $(document).ready( function () {
//             var ticketTable = $('#ticket-table').dataTable( {
//                 "fnDrawCallback": function() {
//                     // Initialize popovers anytime new data is loaded into the table
//                     $('a[rel=tooltip]').tooltip({
//                         placement: 'left'
//                     });
//                 },
//                 "bServerSide": true,
//                 "bAutoWidth": false,
//                 "sPaginationType": "bootstrap",
//                 "sAjaxSource": "{% url get_tickets_list %}",
//                 "aaSorting": [[ 2, "desc" ]],
//                 "iPageLength": 25,
//                 "bLengthChange": false,
//                 "bStateSave": true,
//                 "bFilter": true,
//                 "sDom": "<'length-change'><'row'<'span6'l><'span6'f>r>t<'row'<'span6'i><'length-change'><'span6'p>>",
//                 "oLanguage": {
//                     "sSearch": ""
//                 },
//                 "aoColumns": [
//                     { "bSortable": false, "sWidth": "14px", "bSearchable": false },
//                     { "sWidth": "160px", "bSearchable": true },
//                     { "sWidth": "60px", "bSearchable": true },
//                     { "bSearchable": true },
//                     { "bSortable": false, "sWidth": "14px", "bSearchable": false },
//                     { "sWidth": "50px", "sClass": "center", "bSearchable": false },
//                     { "bSearchable": true },
//                     { "sWidth": "70px", "sClass": "center", "bSearchable": false },
//                     { "sWidth": "75px", "bSearchable": true }
//                 ] } ).fnSetFilteringDelay(500);
//     }
// );