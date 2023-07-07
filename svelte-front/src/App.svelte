<script lang="ts">
  // From https://svelte.dev/repl/36aaf2a1807a4fed81fe6212d20bca24?version=3.25.1
  import { onMount } from 'svelte';
  
  import ViewSelectionFrame from './VueSelectionFrame.svelte';
  import EditFrame from './EditFrame.svelte';
  import Login from './Login.svelte';
  import Table from './Table.svelte';
  import { auth } from './authentification'
  import { apiActionRequest, getCookie, getMeta } from './main'

  import "carbon-components-svelte/css/g100.css";
  /* Notes:
  When update fails, the row is not updated in the backend, but the frontend is updated
  No undo button yet
  
  */

  let columnNames = ['11111111111111111111', '11111111111111111111', '11111111111111111111'];
  let tableData = [];
  const csrfToken = getMeta('csrf-token');
 
  onMount(async () => {
    await auth();
    let jwt = getCookie('jwt')
    apiActionRequest(csrfToken, jwt, 'fetch_all', 'view_1', [], []).then((res) => {
      columnNames = res.names
      tableData = res.table;
    })
  });
  let theme = "g100"; // "white" | "g10" | "g80" | "g90" | "g100"
  $: document.documentElement.setAttribute("theme", theme);
</script>

<svelte:head>
	<!-- <link rel="stylesheet" href="//cdn.datatables.net/1.13.5/css/jquery.dataTables.min.css" /> -->
  
</svelte:head>

<div class="app-container">
  <Login />
  <ViewSelectionFrame />
  <div class="side-container">
    <Table tableData={tableData} columnNames={columnNames}/>
    <EditFrame />
  </div>
</div>

<style>
  .side-container {
    display: flex;
    transform: translateX(-500px);
    flex-direction: row;
    align-items: start;
    justify-content: start;
    overflow: hidden;
    width: fit-content;
  }
  .app-container {
    width: fit-content;
    display: flex;
    flex-direction: row;
    align-items: start;
    justify-content: start;
    overflow: hidden;
    height: 100vh;
  }
</style>