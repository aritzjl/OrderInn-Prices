const errorElement = document.getElementById('error');

if (errorElement && typeof errorElement.value === 'string' && errorElement.value.trim() !== '') {
  const errorMessage = errorElement.value;
  if (typeof Swal === 'undefined') {
    console.error('SweetAlert2 library is not loaded');
  } else {
    Swal.fire({
      icon: 'error',
      title: errorMessage,
      showConfirmButton: true,
      timer: 20000,
      confirmButtonColor: '#d1ff4f'
    });
  }
}