const checkForm = (form) => {
  var valid = form.checkValidity();
  if (!valid) {
    event.preventDefault();
    event.stopPropagation();
  }
  form.classList.add("was-validated");
  return valid;
};
