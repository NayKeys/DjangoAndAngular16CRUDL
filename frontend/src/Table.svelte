<script lang="ts">
  /*
  SEE: https://github.com/dhobi/datatables.colResize for column resizing implementation
  */
  import s from 'jquery'
	import { onMount, tick } from 'svelte'
	import DataTable from 'datatables.net-dt'
	import type { Api }from 'datatables.net-dt'
  import 'datatables.net-buttons-dt';
  import 'datatables.net-fixedheader-dt';
  import 'datatables.net-keytable-dt';
  import 'datatables.net-responsive-dt';
  import 'datatables.net-scroller-dt';
  import 'datatables.net-searchbuilder-dt';
  import 'datatables.net-select-dt';
  import { TextInputSkeleton } from "carbon-components-svelte";

  import { getMeta, getCookie } from './requests'
  import type { RowKeys, RowValues } from './requests'
  import { apiActionRequest } from './requests';
	import Button from './Button.svelte';

  export let showRowCreation: () => void;
  export let deleteRows: (rows: RowValues[]) => void;
  export let columnNames: RowKeys = []
  export let tableData: RowValues[] = []
  export let selectedData: RowValues[] = []
  export let showEditFrame: (e: any) => void;
  export let hideEditFrame: (e: any) => void;
  
  let newRow: RowValues = [];
  let table: Api<any>;

  function deleteSelectedRows() {
    deleteRows(selectedData)
  }
  
  onMount(async () => {
    s('#table tfoot th').each(function() {
      let title = s(this).text();
      s(this).html('<input type="text" placeholder="Search ' + title + '" />');
    });
    table = new DataTable('#table', {
      search: {
        return: false,
      },
      responsive: true,
      paging: true,
      scrollCollapse: true,
      scrollX: true,
      ordering: true,
      scrollY: "620px",
      select: true,
      pageLength: 200,
      dom: 'Plfrtip',
      searchPanes: {
        viewTotal: true
      },
      buttons: ['add', 'delete'],
    });
    table.on( 'select', function ( e, dt, type, indexes )  {
      selectedData = table.rows({selected: true}).data().toArray() as RowValues[];
      if (selectedData.length == 1)
        showEditFrame(e)
      else
        hideEditFrame(e)
    })
    table.columns().every(function() {
      const that = this;
      s('input', this.footer()).on('keyup change', function() {
        if (that.search() !== this.value) {
          that.search(this.value).draw();
        }
      });
    });
    table.columns.adjust().draw();
    s('.table').css({"width":"100%"});
    //Editing the datatable
    s('#table_length')[0].remove()
    s('#table_wrapper')[0].prepend(s('.table-buttons')[0]);
    s('#table_filter')[0].prepend(s('#search-vector')[0]); 
    
    //Editing table filter (the searchbar)
    s('#table_wrapper .table-buttons')[0].prepend(s('#table_filter')[0]);
    s('#table_filter')[0].classList.add('lexenddeca-normal-oslo-gray-24px');  // Changing fonts (unnecessary)
    s('#table_filter')[0].appendChild(s('#table_filter label input')[0]);  // Moving input out of label
    s('#table_filter label')[0].remove()  // Cringe useless label
    s('#table_filter input')[0].classList.add('lexenddeca-normal-oslo-gray-24px');  // Unnecessary again
    s('#table_filter input')[0].attributes.placeholder.value = 'Search'  // Ignore TS error
    
    s('thead tr th').each((i, e) => {
      const correspondingWidth:string = s(s(`#table tfoot tr th`)[i]).css('width');
      s(e).css({"width": correspondingWidth})
    })
    s(document).on('keyup', function (e) {
      const target = e.target as HTMLElement|Document;
      if (target instanceof HTMLElement)
      if (target.tagName === 'INPUT')
      return;
      if (e.keyCode >= 48 && e.keyCode <= 57) {
        // Number
        table.search(e.key).draw();
        s('#table_filter input').trigger('focus')
      } else if (e.keyCode >= 65 && e.keyCode <= 90) {
        // Alphabet upper case
        table.search(e.key).draw();
        s('#table_filter input').trigger('focus')
      } else if (e.keyCode >= 97 && e.keyCode <= 122) {
        // Alphabet lower case
        table.search(e.key).draw();
        s('#table_filter input').trigger('focus')
      }
    });
  });
</script>

<svelte:head>
	<!-- <link rel="stylesheet" href="//cdn.datatables.net/1.13.5/css/jquery.dataTables.min.css" /> -->
</svelte:head>

<div class="frame-31">
  <h1 class="vue-tudiants-1re-anne valign-text-middle">Vue étudiants 1ère année</h1>
  <div class="top-seperator"></div>
</div>
<img id="search-vector" class="vector" src="https://anima-uploads.s3.amazonaws.com/projects/63f7f6d546da9210f99dd5aa/releases/64a3f5479ef0ce55861f0160/img/vector.svg" alt="Vector" />
<div class="table-buttons">
  <Button onClick={showRowCreation} class="add-button" width={35} text="Add" fill={false}>
    <svg class="button-vector" viewBox="0 0 38 44" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M23.2311 25.0864L14.83 16.6854M23.1331 16.7843L14.7319 25.1855M15.9954 2.92749L6.13139 6.64376C3.85814 7.49376 2 10.1821 2 12.5937V27.281C2 29.6136 3.54186 32.6775 5.41976 34.081L13.9197 40.4263C16.707 42.5217 21.293 42.5217 24.0803 40.4263L32.5802 34.081C34.4581 32.6775 36 29.6136 36 27.281V12.5937C36 10.1624 34.1419 7.47399 31.8686 6.62399L22.0047 2.92749C20.3244 2.3147 17.6361 2.3147 15.9954 2.92749Z" stroke-width="3" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  </Button>
  <Button onClick={() => deleteSelectedRows()} class="delete-button" width={35} text="Delete" fill={false} >
    <svg class="button-vector" viewBox="0 0 38 44" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M23.2311 25.0864L14.83 16.6854M23.1331 16.7843L14.7319 25.1855M15.9954 2.92749L6.13139 6.64376C3.85814 7.49376 2 10.1821 2 12.5937V27.281C2 29.6136 3.54186 32.6775 5.41976 34.081L13.9197 40.4263C16.707 42.5217 21.293 42.5217 24.0803 40.4263L32.5802 34.081C34.4581 32.6775 36 29.6136 36 27.281V12.5937C36 10.1624 34.1419 7.47399 31.8686 6.62399L22.0047 2.92749C20.3244 2.3147 17.6361 2.3147 15.9954 2.92749Z" stroke-width="3" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  </Button>
</div>
<div class="table-container">
  <table id="table" class="dataTable table hover order-column row-border">
    <thead>
      <tr class="row-1">
        {#each columnNames as column}
          <th class="">
            {column}
          </th>
        {/each}
      </tr>
    </thead>
    <tbody>
      {#if tableData.length == 0}
        {#each {length: 15} as _, i}
          <tr class="row">
            {#each {length: 3} as _, i}
              <th class="">
                <TextInputSkeleton hideLabel />
              </th>
            {/each}
          </tr>
        {/each}
      {/if}
      {#each tableData as row}
        <tr class="row">
          {#each row as cell}
            <th class="">
              {cell}
            </th>
          {/each}
        </tr>
      {/each}
    </tbody>
    <tfoot class="footer">
      <tr>
        {#each columnNames as column}
          <th class="footer-search">
            <div class="">
              <div class="footer">
                {column}
              </div>
            </div>
          </th>
        {/each}
      </tr>
    </tfoot>
  </table>
</div>

<style>
  :global(:root) {
    --specialred: #95312A;
  }
  :global(.button.delete-button:hover .button-vector, .button.delete-button:hover .button-label) {
    stroke: var(--specialred) !important;
    color: var(--specialred) !important;
  }
  :global(.button.delete-button:active .button-vector, .button.delete-button:active .button-label) {
    stroke: var(--whitetext) !important;
    color: var(--whitetext) !important;
  }
  :global(.button.add-button:hover .button-vector, .button.add-button:hover .button-label) {
    stroke: var(--specialcolor) !important;
    color: var(--specialcolor) !important;
  }
  :global(.button.add-button:active .button-vector, .button.add-button:active .button-label) {
    stroke: var(--whitetext) !important;
    color: var(--whitetext) !important;
  }
  .table-buttons {
    margin-bottom: 12px;
  }
  .table-container {
    width: 100%;
    overflow-x: hidden;
  }
  .table {
    height: 100%;
    overflow: hidden;
  }
  .row-1 {
    height: 51px;
    font-size: 1rem;
    color: var(--darkcontroltext);
    font-family: var(--font-family-lexend_deca);
    font-weight: 400;
  }
  .row {
    height: 46px;
    font-size: 1.2rem;
    color: var(--whitetext);
    font-family: var(--font-family-lexend_deca);
    font-weight: 400;
  }
  .table-buttons {
    align-items: center;
    align-self: stretch;
    display: flex;
    gap: 37px;
    position: relative;
  }
  .valign-text-middle {
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  .vector {
    height: 31px;
    min-width: 31px;
    position: relative;
  }
  .frame-31 {
    align-items: flex-start;
    display: flex;
    flex-direction: column;
    gap: 8px;
    justify-content: center;
    position: relative;
      width: 100%;
  }
  .vue-tudiants-1re-anne {
    color: #d7dde6;
    font-family: var(--font-family-lexend_deca);
    font-size: var(--font-size-l3);
    font-weight: 400;
    height: 31px;
    letter-spacing: 0;
    line-height: normal;
    margin-top: -1px;
    position: relative;
  }
  .top-seperator {
    background-color: var(--bright-gray);
    border-radius: 10px;
    height: 4px;
    min-width: 95%;
    position: relative;
  }
</style>