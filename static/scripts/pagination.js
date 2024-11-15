function updatePageSizeSelector() {
  const urlParams = new URLSearchParams(window.location.search);
  const pageSize = urlParams.get('page_size');
  const paginationSelect = document.getElementById('pagination');

  if (pageSize) {
    paginationSelect.value = pageSize;
  }

  paginationSelect.addEventListener('change', function(event) {
    const newPageSize = event.target.value;
    const url = new URL(window.location.href);
    url.searchParams.delete('page');
    url.searchParams.set('page_size', newPageSize);
    window.location.href = url.href;
  });
}

document.addEventListener('DOMContentLoaded', updatePageSizeSelector);
