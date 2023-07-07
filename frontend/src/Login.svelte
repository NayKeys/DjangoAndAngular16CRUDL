<script lang='ts'>
  import { auth } from './authentification'
  import { onMount } from 'svelte';
  import { getMeta, getCookie, setCookie } from './requests'
  
  let error:string = ''

  onMount(async () => {
  });
</script>

{#if error}
  <p>{error}</p>
{/if}
