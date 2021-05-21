//Function on click that triggers a task in the view file.

$('.button').on('click', function() {
    $.ajax({
      url: '/tasks/',
      data: { type: $(this).data('type') },
      method: 'POST',
    })
    .done((res) => {
      getStatus(res.task_id);
    })
    .fail((err) => {
      console.log(err);
    });
  });