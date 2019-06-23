function close_modal(id) {
    // Find the modal with the given ID
    let image_modal = document.getElementById(id);
    // Remove the open-modal class from the modal
    image_modal.classList.remove("open-modal");

}

function open_modal(id) {
    // Find the modal with the given ID
    let image_modal = document.getElementById(id);
    // Add the open-modal class to the modal
    image_modal.classList.add("open-modal");

}