<script lang="ts">
  // From https://svelte.dev/repl/36aaf2a1807a4fed81fe6212d20bca24?version=3.25.1
  import { onMount } from 'svelte';
  
  import Login from './Login.svelte';
  import Table from './Table.svelte';
  import ViewSelectionFrame from './ViewSelectionFrame.svelte';
  import EditFrame from './EditFrame.svelte';
  
  import { auth } from './authentification'
  /* Notes:
  When update fails, the row is not updated in the backend, but the frontend is updated
  No undo button yet
  
  */
  onMount(async () => {
    // await auth();
  });
</script>

<div class="app-container">
  <Login />
  <ViewSelectionFrame />
  <Table />
  <EditFrame />
</div>

<style>
  .app-container {
    display: flex;
    flex-direction: row;
    align-items: start;
    justify-content: start;
    overflow: hidden;
    height: 100vh;
  }
</style>