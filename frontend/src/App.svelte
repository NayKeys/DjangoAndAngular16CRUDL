<script lang="ts">
  // From https://svelte.dev/repl/36aaf2a1807a4fed81fe6212d20bca24?version=3.25.1
  import { onMount } from 'svelte';
  
  import ViewSelectionFrame from './VueSelectionFrame.svelte';
  import EditFrame from './EditFrame.svelte';
  import CreationFrame from './CreationFrame.svelte';
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
  let viewTree: ViewTree;
  let selectedData: RowValues[] = [];
  let showEditFrame: boolean = false;
  let createMode: boolean = false;
  let view_path: string;
  let rerenderTable:boolean = false;

  function areRowEquals(row1: RowValues, row2: RowValues) {
    for (let i = 0; i < row1.length; i++) {
      if (row1[i].toString() !== row2[i].toString()) {
        return false;
      }
    }
    return true;
  }
  
  function fetchViewData (path : string) {
    if (path) {
      view_path = path
      apiActionRequest('fetch_all', path, [], []).then((res) => {
        columnNames = res.names
        tableData = res.table;
        rerenderTable = !rerenderTable;
      });
    }
  }

  function addRow(keys: RowKeys, newRow: RowValues) {
    if (view_path)
      apiActionRequest('create', view_path, keys, newRow).then((res) => {
        if (res != undefined) {
          fetchViewData(view_path)
        }
      })
	}

	function deleteRows(rowsToBeDeleted: RowValues[]) {
    if (view_path)
      for (let rowToBeDeleted of rowsToBeDeleted) {
        apiActionRequest('remove', view_path, columnNames, rowToBeDeleted).then((res) => {
          if (res != undefined) {
            tableData = tableData.filter(row => !areRowEquals(row, rowToBeDeleted))
            rerenderTable = !rerenderTable;
            showEditFrame = false;
            createMode = false;
          }
        })
      }
	}

  function updateRow(oldRow: RowValues, newRow: RowValues) {
    if (view_path)
      apiActionRequest('update', view_path, columnNames, newRow).then((res) => {
        if (res != undefined) {
          for (let i in tableData) {
            if (areRowEquals(tableData[i], oldRow)) {
              tableData[i] = newRow
            }
          }
          rerenderTable = !rerenderTable;
        }
      })
  }
 
  function showRowCreation() {
    createMode = true;
    showEditFrame = true;
  }
  
  onMount(async () => {
    await auth();
    apiTreeRequest().then((res) =>  {
      viewTree = res;
    });
  });
  let theme = "g100"; // "white" | "g10" | "g80" | "g90" | "g100"
  $: document.documentElement.setAttribute("theme", theme);
</script>

<svelte:head>
	<!-- <link rel="stylesheet" href="//cdn.datatables.net/1.13.5/css/jquery.dataTables.min.css" /> -->
  
</svelte:head>

<div class="app-container">
  <div class="left-container">
    <Login />
    <div class="view-selection-frame" on:click={() => (showEditFrame = false)} on:keypress>
      <ViewSelectionFrame viewTree={viewTree} fetchViewData={fetchViewData}/>
    </div>
  </div>
  <div class="side-container">
    <div id="table-frame" class="table-frame screen" on:click|self={() => (showEditFrame = false)} on:keypress={() => (true)}>
      {#key rerenderTable}
        <Table showRowCreation={showRowCreation} deleteRows={deleteRows} columnNames={columnNames} bind:selectedData={selectedData} tableData={tableData} showEditFrame={() => (showEditFrame = true)} hideEditFrame={() => (showEditFrame = false)} />
      {/key}
    </div>
  </div>
  <div class="relative">
    <div class={`edit-frame screen ${showEditFrame ? 'unmoved' : 'toright'}`} >
      {#if createMode}
        <CreationFrame addRow={addRow} hideCreationFrame={() => {showEditFrame=false; createMode=false}} columnNames={columnNames} />
      {:else}
        {#key tableData}
          {#key selectedData}
            <EditFrame updateRow={updateRow} deleteRows={deleteRows} hideEditFrame={() => (showEditFrame=false)} columnNames={columnNames} oldRow={selectedData[0]} />
          {/key}
        {/key}
      {/if}
    </div>
  </div>
</div>

<style>
  .toleft {
    transform: translateX(-100%);
  }
  .unmoved {
    transform: translateX(0px);
  }
  .toright {
    transform: translateX(100%);
  }
  .side-container {
    display: flex;
    transform: translateX(0px);
    transition: transform 0.3s ease-in-out;
    flex-direction: row;
    align-items: start;
    justify-content: start;
    width: 100%;
    width: stretch;             /* Unprefixed */
    width: -webkit-fill-available;  /* For Chrome */
    width: -moz-available;          /* For Mozzila */
  }
  .left-container {
    width: fit-content;
  }
  .app-container {
    position: relative;
    width: 100vw;
    height: 100vh;
    display: flex;
    flex-direction: row;
    align-items: start;
    justify-content: start;
    overflow-x: hidden;
    overflow-y: hidden;
  }
  .view-selection-frame {
    align-items: center;
    background-color: var(--eerie-black);
    border: 1px none;
    display: flex;
    flex-direction: column;
    gap: 21px;
    padding: 25px;
    position: relative;
    width: fit-content;
    height: 100vh;
    overflow: scroll;
  }
  .edit-frame {
    align-items: center;
    background-color: #14181b;
    position: absolute;
    top: 0;
    right: 0;
    border: 1px none;
    display: flex;
    flex-direction: column;
    gap: 31px;
    padding: 30px 0;
    width: 738px;
    height: 100vh;
    overflow-y: scroll;
    transition: transform 0.4s ease-in-out;
  }
  .table-frame {
    position: relative;
    align-items: flex-start;
    background-color: var(--shark);
    border: 1px none;
    display: flex;
    flex-direction: column;
    gap: 50px;
    justify-content: center;
    padding: 25px;
    width: 67vw;
  }
</style>