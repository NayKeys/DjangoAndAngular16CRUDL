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

  import type { RowKeys, RowValues } from './requests'
	import Button from './Button.svelte';

  export let showRowCreation: () => void;
  export let deleteRows: (rows: RowValues[]) => void;
  export let columnNames: RowKeys = []
  export let tableData: RowValues[] = []
  export let selectedData: RowValues[] = []
  export let showEditFrame: (e: any) => void;
  export let hideEditFrame: (e: any) => void;
  export let viewName: string = "View";
  
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
  <h1 class="vue-tudiants-1re-anne valign-text-middle">{viewName.toLocaleUpperCase()}</h1>
  <div class="top-seperator"></div>
</div>
<img id="search-vector" class="vector" src="https://anima-uploads.s3.amazonaws.com/projects/63f7f6d546da9210f99dd5aa/releases/64a3f5479ef0ce55861f0160/img/vector.svg" alt="Vector" />
<div class="table-buttons">
  <Button onClick={showRowCreation} class="add-button" width={37} text="New Row" textHeight={20} fill={false}>
    <svg class="button-vector" xmlns="http://www.w3.org/2000/svg" width="37" height="37" fill="none" viewBox="0 0 69 69">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="4.726" d="M25.056 66.016H43.96c15.754 0 22.055-6.301 22.055-22.055V25.056C66.016 9.302 59.715 3 43.961 3H25.056C9.302 3 3 9.302 3 25.056V43.96c0 15.754 6.302 22.055 22.056 22.055Zm-3.151-31.508H47.11M34.508 47.111V21.905"/>
    </svg>
  </Button>
  <Button onClick={() => deleteSelectedRows()} class="delete-button" width={37} text="Delete" textHeight={20} fill={true} confirmation="Are you sure you want to delete those {selectedData.length} elements ? This action is irreversible." >
    <svg class="button-vector" xmlns="http://www.w3.org/2000/svg" width="37" height="37" fill="none" viewBox="0 0 64 76">
      <path d="M27.647.583 7.127 8.269C3.208 9.76 0 14.388 0 18.604v30.22c0 3.023 1.977 7.015 4.403 8.806l20.52 15.334c3.62 2.724 9.551 2.724 13.17 0l20.52-15.334c2.426-1.828 4.403-5.783 4.403-8.805V18.604c0-4.179-3.208-8.843-7.126-10.298L35.37.62C33.28-.2 29.773-.2 27.647.583Z" opacity=".4"/>
      <path d="m41.526 41.063-5.933-5.932 5.783-5.783a2.815 2.815 0 0 0 0-3.955 2.815 2.815 0 0 0-3.954 0l-5.783 5.783-5.933-5.932a2.815 2.815 0 0 0-3.954 0 2.815 2.815 0 0 0 0 3.955l5.932 5.932-6.12 6.12a2.815 2.815 0 0 0 0 3.954c.56.56 1.27.82 1.978.82.71 0 1.418-.26 1.978-.82l6.119-6.119 5.932 5.932c.56.56 1.268.821 1.977.821a2.77 2.77 0 0 0 1.978-.82c1.082-1.12 1.082-2.873 0-3.956Z"/>
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
  :global(#table thead) {
  display: none;
  }
  :global(.footer .footer-search > *:focus-visible) {
    outline: none;
    border: 1px solid var(--specialcolor);
  }
  :global(.footer .footer-search > *) {
    border: 0px solid var(--whitetext);
    border-radius: 2px;
    background-color: var(--lightbackground);
    color: var(--whitetext);
  }
  :global(thead tr th) {
    vertical-align: middle;
  }
  :global(#table th) {
  text-align: start;
  flex: 1;
  letter-spacing: 0;
  line-height: 28px;
  margin-top: -1px;
  position: relative;
  white-space: nowrap;
  padding-bottom: 4px;
  padding-top: 4px;
}
:global(table.dataTable tbody tr.selected .dtr-control::before) {
  background-color: var(--specialcolor);
  position: absolute;
  top: 0;
  left: 0;
  width: .25rem;
  height: 100%;
  content: "";
}
:global(table.dataTable tbody tr.selected .dtr-control) {
  position: relative;
}
:global(table.dataTable tbody tr.selected > *) {
  box-shadow: inset 0 0 0 9999px rgba(55, 65, 73, 0.9);
  box-shadow: inset 0 0 0 9999px rgba(var(--dt-row-selected), 0.9);
  color: white;
  color: rgb(var(--dt-row-selected-text));
}
:global(#table_wrapper) {
  width: 100%;
  overflow-x: hidden;
  gap: 100px;
}
:global(#table_filter) {
  left: 0px;
  float: left !important;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: end;
  width: 748px;
  background-color: var(--eerie-black);
  border: 2px solid;
  border-color: var(--bright-gray);
  border-radius: 5px;
}
:global(#table_filter:focus-within) {
  border-color: var(--specialcolor);
}
:global(#table_filter input:focus-visible) {
  outline: none;
}
:global(#table_filter input) {
  margin: 0px;
  color: var(--white);
  background-color: var(--eerie-black);
  border: 0px solid;
  align-items: center;
  line-height: 31px;
  display: flex;
  gap: 12px;
  padding: 12px 15px;
  position: relative;
  width: 94%;
}
:global(#table_info) {
  color: var(--darkcontroltext);
}
:global(#table_paginate > )*{
  color: var(--darkcontroltext);
}
:global(#table_paginate > * > *) {
  color: var(--darkcontroltext);
}
:global(#table_previous:hover, #table_previous:active) {
  color: var(--whitetext);
  background: var(--darkselected);
}
:global(#table_next:hover, #table_previous:active) {
  color: var(--whitetext);
  background: var(--darkselected);
}
  :global(:root) {
    --specialred: #95312A;
  }
  :global(.button.delete-button:hover .button-vector, .button.delete-button:hover .button-label) {
    fill: var(--specialred) !important;
    color: var(--specialred) !important;
  }
  :global(.button.delete-button:active .button-vector, .button.delete-button:active .button-label) {
    fill: var(--whitetext) !important;
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