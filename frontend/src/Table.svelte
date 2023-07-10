<script lang="ts">
  /*
  SEE: https://github.com/dhobi/datatables.colResize for column resizing implementation
  */
  import s from 'jquery'
	import { onMount, tick } from 'svelte'
	import DataTable from 'datatables.net-dt'
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

  export let columnNames: RowKeys = []
  export let tableData: RowValues[] = []
  
  let newRow: RowValues = [];
  const csrfToken = getMeta('csrf-token');
  let jwt = getCookie('jwt');
  
	function addRow() {
    apiActionRequest(csrfToken, jwt, 'create', 'view_1', columnNames, newRow).then((res) => {
      if (res != undefined) {
        tableData = [...tableData, [...newRow]]
      }
    })
	}
	function deleteRow(rowToBeDeleted: RowValues) {
    apiActionRequest(csrfToken, jwt, 'remove', 'view_1', columnNames, rowToBeDeleted).then((res) => {
      if (res != undefined) {
        tableData = tableData.filter(row => row != rowToBeDeleted)
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
    s('#table tfoot th').each(function() {
        let title = s(this).text();
        s(this).html('<input type="text" placeholder="Search ' + title + '" />');
    });
    let table = new DataTable('#table', {
      responsive: true,
      search: {
        return: false
      },
      scrollX: true,
      paging: true,
      ordering: true,
      scrollY: "720px",
      select: true,
      pageLength: 50,
      fixedHeader: true,
      searchPanes: {
        viewTotal: true
      },
      dom: 'Plfrtip'
    });
    table.columns().every(function() {
      const that = this;
      s('input', this.footer()).on('keyup change', function() {
        if (that.search() !== this.value) {
          that.search(this.value).draw();
        }
      });
    });
    //Editing the datatable
    s('#table_length')[0].remove()  // Not using that
    s('#table_wrapper')[0].prepend(s('.table-buttons')[0]);
    s('#table_filter')[0].prepend(s('#search-vector')[0]); 
    
    //Editing table filter (the searchbar)
    s('#table_wrapper .table-buttons')[0].prepend(s('#table_filter')[0]);
    s('#table_filter')[0].classList.add('lexenddeca-normal-oslo-gray-24px');  // Changing fonts (unnecessary)
    s('#table_filter')[0].appendChild(s('#table_filter label input')[0]);  // Moving input out of label
    s('#table_filter label')[0].remove()  // Cringe useless label
    s('#table_filter input')[0].classList.add('lexenddeca-normal-oslo-gray-24px');  // Unnecessary again
    s('#table_filter input')[0].attributes.placeholder.value = 'Search'  // Ignore TS error

    s(document).on('keyup', function (event) {
      const target = event.target as HTMLElement|Document;
      console.log(target)
      if (target instanceof HTMLElement)
      if (target.tagName === 'INPUT')
      return;
      table.search(event.key).draw();
      s('#table_filter input').trigger('focus')
    });
  });
  // bind:this={table}
</script>

<svelte:head>
	<!-- <link rel="stylesheet" href="//cdn.datatables.net/1.13.5/css/jquery.dataTables.min.css" /> -->
</svelte:head>

<div id="table-frame" class="table-frame screen">
  <div class="frame-31">
    <h1 class="vue-tudiants-1re-anne valign-text-middle">Vue étudiants 1ère année</h1>
    <div class="top-seperator"></div>
  </div>
  <img id="search-vector" class="vector" src="https://anima-uploads.s3.amazonaws.com/projects/63f7f6d546da9210f99dd5aa/releases/64a3f5479ef0ce55861f0160/img/vector.svg" alt="Vector" />
  <div class="table-buttons">
    <div class="filter">
      <img class="vector-1" src="https://anima-uploads.s3.amazonaws.com/projects/63f7f6d546da9210f99dd5aa/releases/64a3f5479ef0ce55861f0160/img/vector-1.svg" alt="Vector" />
      <div class="filter-1 valign-text-middle lexenddeca-normal-oslo-gray-24px">Filter</div>
      <div class="frame-31-1"><div class="number valign-text-middle lexenddeca-normal-oslo-gray-24px">7</div></div>
    </div>
    <div class="sort">
      <img class="vector-2" src="https://anima-uploads.s3.amazonaws.com/projects/63f7f6d546da9210f99dd5aa/releases/64a3f5479ef0ce55861f0160/img/vector-2.svg" alt="Vector" />
      <div class="sort-1 valign-text-middle lexenddeca-normal-oslo-gray-24px">Sort</div>
    </div>
  </div>
  <div class="table-container">
    <table id="table" class="dataTable table hover order-column row-border">
      <thead>
        <tr class="row-1">
          {#each columnNames as column}
            <th class="">
              <div class="">
                <div class="text">
                  {column}
                </div>
              </div>
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
                  <div class="content">
                    <div class="text">
                      <TextInputSkeleton hideLabel />
                    </div>
                  </div>
                </th>
              {/each}
            </tr>
          {/each}
        {/if}
        {#each tableData as row}
          <tr class="row">
            {#each row as cell}
              <th class="">
                <div class="content">
                  <div class="text">
                    {cell}
                  </div>
                </div>
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
</div>

<style>
  .table-buttons {
    margin-bottom: 12px;
  }
  .table-container {
    height: 900px;
  }
  .table {
    height: 100%;
    overflow: hidden;
  }
  .content {
    padding-bottom: 4px;
    padding-top: 4px;
  }
  .text {
    text-align: start;
    flex: 1;
    letter-spacing: 0;
    line-height: 28px;
    margin-top: -1px;
    position: relative;
    white-space: nowrap;
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
  .table-frame {
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
  .table-buttons {
    align-items: center;
    align-self: stretch;
    display: flex;
    gap: 37px;
    position: relative;
  }
  .sort {
    align-items: center;
    background-color: var(--eerie-black);
    border: 2px solid;
    border-color: var(--bright-gray);
    border-radius: 5px;
    display: flex;
    gap: 8px;
    justify-content: center;
    padding: 12px 16px;
    position: relative;
    width: fit-content;
  }
  .vector-2 {
    height: 24.98px;
    margin-left: -2.5px;
    min-width: 40.96px;
    position: relative;
  }
  .valign-text-middle {
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  .sort-1 {
    height: 31px;
    letter-spacing: 0;
    line-height: normal;
    margin-top: -2px;
    position: relative;
    width: 53px;
  }
  .vector {
    height: 31px;
    min-width: 31px;
    position: relative;
  }
  .filter {
    align-items: center;
    background-color: var(--eerie-black);
    border: 2px solid;
    border-color: var(--bright-gray);
    border-radius: 5px;
    display: flex;
    gap: 8px;
    padding: 8px;
    position: relative;
    width: fit-content;
  }
  .filter-1 {
    height: 31px;
    letter-spacing: 0;
    line-height: normal;
    position: relative;
    width: 67px;
  }
  .frame-31-1 {
    align-items: center;
    background-color: #2a944780;
    border-radius: 5px;
    display: flex;
    justify-content: center;
    overflow: hidden;
    position: relative;
    width: fit-content;
  }
  .number {
    height: 31px;
    letter-spacing: 0;
    line-height: normal;
    margin-top: -1px;
    position: relative;
    text-align: center;
    width: 31px;
  }
  .vector-1 {
    height: 38.1px;
    min-width: 33.48px;
    position: relative;
  }
  .frame-31 {
    align-items: flex-start;
    display: flex;
    flex-direction: column;
    gap: 8px;
    justify-content: center;
    position: relative;
    width: fit-content;
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
    min-width: 1114px;
    position: relative;
  }
</style>