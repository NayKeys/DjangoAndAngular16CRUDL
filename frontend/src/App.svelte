<script lang="ts">
  // From https://svelte.dev/repl/36aaf2a1807a4fed81fe6212d20bca24?version=3.25.1
  import { onMount } from 'svelte';
  
  import ViewSelectionFrame from './VueSelectionFrame.svelte';
  import EditFrame from './EditFrame.svelte';
  import Login from './Login.svelte';
  import Table from './Table.svelte';
  import { auth } from './authentification'
  import { apiActionRequest, getCookie, apiTreeRequest, getMeta } from './requests'
  import type { RowKeys, RowValues, ViewTree } from './requests'
  import j from 'jquery'

  import "carbon-components-svelte/css/g100.css";
  /* Notes:
  When update fails, the row is not updated in the backend, but the frontend is updated
  No undo button yet
  
  */

  let columnNames = ['----------------------------', '----------------------------', '----------------------------'];
  let tableData = [];
  const csrfToken = getMeta('csrf-token');
  let jwt = getCookie('jwt')
  let viewTree: ViewTree;
  let selectedData: RowValues = [];

  function fetchViewData (path : string) {
    if (path) {
      apiActionRequest(csrfToken, jwt, 'fetch_all', path, [], []).then((res) => {
        columnNames = res.names
        tableData = res.table;
      });
    }
  }
 
  onMount(async () => {
    await auth();
    apiTreeRequest(csrfToken).then((res) =>  {
      viewTree = res;
    });
  });
  let theme = "g100"; // "white" | "g10" | "g80" | "g90" | "g100"
  $: document.documentElement.setAttribute("theme", theme);
  function showLeft(event) {
    j('.side-container').css('transform', 'translateX(0px)');
  }
  function showRight(event) {
    if ((event.key && event.key == "ArrowRight") || event.type == "click")
      j('.side-container').css('transform', 'translateX(-360px)');
  }
</script>

<svelte:head>
	<!-- <link rel="stylesheet" href="//cdn.datatables.net/1.13.5/css/jquery.dataTables.min.css" /> -->
  
</svelte:head>

<div class="app-container">
  <div class="left-container" on:click={showLeft} on:keypress={(event) => showLeft(event)}>
    <Login />
    <ViewSelectionFrame viewTree={viewTree} fetchViewData={fetchViewData}/>
  </div>
  <div class="side-container" on:click={showRight} on:keypress={(event) => showRight(event)}>
    <div id="table-frame" class="table-frame screen">
      {#key tableData}
        <Table bind:selectedData={selectedData} tableData={tableData} columnNames={columnNames}/>
      {/key}
      </div>
    {#key tableData}
      {#key selectedData}
        <div class="edit-frame screen">
          <EditFrame columnNames={columnNames} selectedData={selectedData} />
        </div>
      {/key}
    {/key}
  </div>
</div>

<style>
  .side-container {
    display: flex;
    transform: translateX(0px);
    transition: transform 0.3s ease-in-out;
    flex-direction: row;
    align-items: start;
    justify-content: start;
    width: fit-content;
  }
  .left-container {
    width: fit-content;
  }
  .app-container {
    width: 100vw;
    display: flex;
    flex-direction: row;
    align-items: start;
    justify-content: start;
    overflow-x: hidden;
    overflow-y: hidden;
    height: 100vh;
  }
  .edit-frame {
    align-items: center;
    background-color: #14181b;
    border: 1px none;
    display: flex;
    flex-direction: column;
    gap: 31px;
    padding: 30px 0;
    width: 738px;
    height: 100vh;
    overflow-y: scroll;
  }
  .table-frame {
    position: relative;
    width: 100vw;
    align-items: flex-start;
    background-color: var(--shark);
    border: 1px none;
    display: flex;
    flex-direction: column;
    gap: 50px;
    justify-content: center;
    padding: 25px;
    position: relative;
  }
</style>