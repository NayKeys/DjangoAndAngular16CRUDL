<script lang="ts">
  // From https://svelte.dev/repl/36aaf2a1807a4fed81fe6212d20bca24?version=3.25.1
  import { onMount } from 'svelte';
  import type { RowKeys, RowValues } from './main'
  import { apiActionRequest } from './main';
  import Login from './Login.svelte';
  import Table from './Table.svelte';
  import { getMeta, getCookie } from './main'
  import { auth } from './authentification'
  /* Notes:
  When update fails, the row is not updated in the backend, but the frontend is updated
  No undo button yet
  
  */
  let columnNames = ['ID', 'Username', 'First Name', 'Last Name', 'Role', 'Age', 'Grade', 'Address']
  let table: RowValues[] = [
    ['1', "johnfish22", "John", "Fisher", "student", '22', '1', "21 uwu sur uwu plage"],
    ['2', "sarahfis24", "Sarah", "Fisher", "student", '22', '1', "21 uwu sur uwu plage"],
    ['3', "afshinfi54", "Afshin", "Fisher", "student", '22', '1', "21 uwu sur uwu plage"],
    ['3', "afshinfi54", "Afshin", "Fisher", "student", '22', '1', "21 uwu sur uwu plage"],
    ['3', "afshinfi54", "Afshin", "Fisher", "student", '22', '1', "21 uwu sur uwu plage"],
    ['3', "afshinfi54", "Afshin", "Fisher", "student", '22', '1', "21 uwu sur uwu plage"],
    ['3', "afshinfi54", "Afshin", "Fisher", "student", '22', '1', "21 uwu sur uwu plage"],
    ['3', "afshinfi54", "Afshin", "Fisher", "student", '22', '1', "21 uwu sur uwu plage"],
  ]
  let newRow: RowValues = [];
  const csrfToken = getMeta('csrf-token');
  let jwt = getCookie('jwt');
	function addRow() {
    apiActionRequest(csrfToken, jwt, 'create', 'view_1', columnNames, newRow).then((res) => {
      if (res != undefined) {
        table = [...table, [...newRow]]
      }
    })
	}
	function deleteRow(rowToBeDeleted: RowValues) {
    apiActionRequest(csrfToken, jwt, 'remove', 'view_1', columnNames, rowToBeDeleted).then((res) => {
      if (res != undefined) {
        table = table.filter(row => row != rowToBeDeleted)
      }
    })
	}
  function updateRow(rowToBeEdited: RowValues) {
    apiActionRequest(csrfToken, jwt, 'update', 'view_1', columnNames, rowToBeEdited).then((res) => {
      if (res != undefined) {
      }
    })
  }

  onMount(async () => {
    // await auth()
    jwt = getCookie('jwt')
    // apiActionRequest(csrfToken, jwt, 'fetch_all', 'view_1', [], []).then((res) => {
    //   columnNames = res.names
    //   table = res.table;
    // })
  });
</script>

<Login />
<Table columnNames={columnNames} tableData={table} newRow={newRow} addRow={addRow} updateRow={updateRow} deleteRow={deleteRow}/>

<style>
</style>