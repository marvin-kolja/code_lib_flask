const sleep = (milliseconds) => {
    return new Promise(resolve => setTimeout(resolve, milliseconds))
}
  
$(document).ready(function() {
    // place this within dom ready function
    function reload() {     
        $( ".flex-container" ).load('.flex-container');
        setTimeout(function(){ reload(); }, 2000); 
    }

    // use setTimeout() to execute
    setTimeout(reload, 6000);
  });