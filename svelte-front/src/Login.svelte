<script lang='ts'>
  import { loginWithCAS, validateCASTicket } from './authentification'
  import { onMount } from 'svelte';
  import { getMeta } from './main'
  import { cookieStore } from 'svelte-cookie';

  const jwt = cookieStore.get('jwt');
  const csrfToken = getMeta('csrf-token');
  const casUrl = getMeta('cas-url');
  const returnUrl = window.location.origin + '/api/auth'

  if (!jwt) {
      // User is not authenticated, redirect to CAS login
      let returnUrl = encodeURIComponent(window.location.origin + '/api/auth');
      window.location.href = casUrl+`?service=${returnUrl}`;
  }
  onMount(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const ticket = urlParams.get('ticket');
    if (ticket) {
      validateCASTicket(ticket);
    }
  });

  const token = localStorage.getItem('jwt');
  fetch('/api/auth', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  })

</script>

<button on:click={loginWithCAS}>Log in with CAS</button>
