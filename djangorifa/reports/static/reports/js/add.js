function add_report_init(map) {
    var lyr = map.layers[1];

    // Register click events
    lyr.events.register('featureselected', lyr, featureSelected);

    // When clicking outside the report form, hide it
    $('#report_map').click(function(e) {
       $('#report_form').hide();
    });

    function formsSubmitHandler() {
        $('#id-report-form').submit(function(e) {
            // Stop default action, serialise the form and send to the server
            e.preventDefault();
            var form = $(this);
            jQuery.ajax({
                type: 'POST',
                data: form.serialize(),
                url: form.attr('action'),
                success: function(data) {
                    $('#id-report-form').html(data);
                }
            });
        });
        $('#id-login-form').submit(function(e) {
           e.preventDefault();
           var form = $(this);
           console.log(form.attr('action'));
           $.ajax({
              type: 'POST',
              data: form.serialize(),
              url: form.attr('action'),
              success: function(data) {
                $('#report_form').html(data).show();
                formsSubmitHandler();
              }
           });
        });
    }

    function featureSelected(event) {
        // If this is a cluster, do nothing
        if(event.feature.cluster.length == 1) {
            // The feature itself is contained within the event feature's cluster
            var pk = event.feature.cluster[0].attributes.pk
            // Get the form for this facility
            jQuery.ajax({
               type: 'GET',
               url: 'facilities/' + pk + '/report/new/',
               success: function(data) {
                   jQuery('#report_form').html(data).show();
                   formsSubmitHandler();
               },
            });
        }
    }

    // Handles what happens when the zoom has changed
    function zoomEnd(event) {
        // When the zoom level is 18, turn off the clustering

        if(event.object.zoom == 18) {

        }
        /*if(event.object.zoom > 16) {
            can_add_report = true;
            var bounds = map.calculateBounds().transform(map.projection, map.displayProjection).toString();
            // Get all the facilities in the current bounds and display them on the map
            jQuery.ajax({
                type:'POST',
                url: '/reports/view/',
                data: {'bounds':bounds},
                success: function(data) {
                    console.log(data);
                },
                dataType: 'json'
            });
        }
        else {
            can_add_report = false;
        }*/
    }
}
