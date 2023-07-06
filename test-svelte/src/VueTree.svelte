<script lang="ts">
  import { TreeView } from "carbon-components-svelte";

  let treeview: TreeView;
  let activeId = "";
  let selectedIds = [];
  let expandedIds = [1, 2, 14];
  let children = [
    { id: 0, text: "AI / Machine learning" },
    {
      id: 101,
      text: "Analytics",
      children: [
        {
          id: 102,
          text: "IBM Analytics Engine",
          children: [
            { id: 3, text: "Apache Spark" },
            { id: 4, text: "Hadoop" },
          ],
        },
        { id: 5, text: "IBM Cloud SQL Query" },
        { id: 6, text: "IBM Db2 Warehouse on Cloud" },
      ],
    },
    {
      id: 107,
      text: "Blockchain",
      children: [{ id: 8, text: "IBM Blockchain Platform" }],
    },
    {
      id: 109,
      text: "Databases",
      children: [
        { id: 10, text: "IBM Cloud Databases for Elasticsearch" },
        { id: 11, text: "IBM Cloud Databases for Enterprise DB" },
        { id: 12, text: "IBM Cloud Databases for MongoDB" },
        { id: 13, text: "IBM Cloud Databases for PostgreSQL" },
      ],
    },
    {
      id: 114,
      text: "Integration",
      disabled: true,
      children: [{ id: 15, text: "IBM API Connect", disabled: true }],
    },
  ];
  const selectItem = (detail) => {
    const id = detail.id
    if (id >= 100) {
      if (expandedIds.includes(id)) {
        expandedIds = expandedIds.filter((i) => i !== id);
      } else {
        expandedIds.push(id);
      }
      console.log(expandedIds)
      treeview?.expandNodes((node) => {
        return expandedIds.includes(node.id as number);
      })
    }
  };
  import j from "jquery" ;
	import { onMount } from "svelte";
  onMount(() => {
    console.log(j('#tree-view')[0].children[1].classList.add('lexenddeca-normal-oslo-gray-20px'))
    for (let key in j('#tree-view')[0].children) {
      console.log(key)
    }
  })
    
</script>

<div id="tree-view">
  <TreeView
    labelText=""
    {children}
    bind:this={treeview}
    bind:activeId
    bind:selectedIds
    on:select={({ detail }) => selectItem(detail)}
  />
</div>

<style>
  div {
    margin-top: var(--cds-spacing-05);
  }
</style>
