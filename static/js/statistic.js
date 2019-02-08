$(document).ready(function(){
  var table = $("#table_id").DataTable();
  var data = table.columns().data();
  var i, Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Des;
  var Mar = 0;
  var Apr = 0;
  for(i in data[2]){
    var txt = data[2][i];
    var split = txt.split(" ");
    var date = split[0];
    var split = date.split("-");
    var month = split[1];
    switch(month){
      case '03':
        Mar += 1;
        break;
      case '04':
        Apr += 1;
        break;
    }
  }
  // window.onload = function() {
  var ctx = $("#myChart");
  var lineChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
      datasets: [{
        label: "2018",
        data: [0, 0, Mar, Apr, 0, 0, 0, 0, 0, 0, 0, 0]
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