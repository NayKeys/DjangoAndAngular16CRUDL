<script lang='ts'>
  import { loginWithCAS, validateCASTicket, validateJWTToken } from './authentification'
  import { onMount } from 'svelte';
  import { getMeta, getCookie, setCookie } from './main'
  let error:string = ''

  onMount(async () => {
    const csrfToken = getMeta('csrf-token');
    const casUrl = getMeta('cas-url');
    const tokenValidationDuration:number = parseInt(getMeta('token-lifetime-hours'));
    const jwt = getCookie('jwt');
    const urlParams = new URLSearchParams(window.location.search);
    const ticket = urlParams.get('ticket');
    if (!jwt && ticket) {  // If no jwt but ticket, verify ticket
      const token = await validateCASTicket(csrfToken, ticket);
      if (!token) {
        error = "Authentification failed."
      } else {
        setCookie('jwt', token, tokenValidationDuration);
      }
    } else if (jwt) {  // If jwt, verify jwt
      validateJWTToken(csrfToken, jwt).then((res) => {
        if (!res) {
          error = "Authentification failed."
        }
      })
    } else {  // Redirecting user to CAS to get ticket
      let returnUrl = encodeURIComponent(window.location.origin);
      window.location.href = casUrl+`?service=${returnUrl}`;
    }
  });
</script>

{#if error}
  <p>{error}</p>
{/if}
```
