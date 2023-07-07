<script lang="ts">
  import { TreeView as Tree} from "carbon-components-svelte";
  import type { ViewTree, View, TreeNode, ViewList } from "./requests";

  export let nodes: TreeNode<View>;
  export let viewPath: string;
  export let fetchViewData;

  let treeview: Tree;
  let activeId = "";
  let selectedIds = [];
  let expandedIds = [1, 2, 14];
  type Node = {
    id: number;
    text: string;
    disabled?: boolean;
    children?: Node[];
  };

  let children:Node[] = []
  let i = 0;
  let paths = {}

  // recursive function to explore the tree and generate the children array
  function exploreTree(node: TreeNode<View>, name: string) {
    if (node['method']) {
      paths[i] = node['path']
      return {id: i++, text: name}
    }
    else {
      let childrenOfNode = []
      for (let [key, value] of Object.entries(node)) {
        childrenOfNode.push(exploreTree(value, key))
      }
      return {id: 100+(i++), text: name, children: childrenOfNode}
    }
  }
  for (let [key, value] of Object.entries(nodes)) {
    children.push(exploreTree(value, key))
  }
  // Parent node with children has id >= 100

  const selectItem = (detail) => {
    const id = detail.id
    if (id >= 100) {
      if (expandedIds.includes(id)) {
        expandedIds = expandedIds.filter((i) => i !== id);
      } else {
        expandedIds.push(id);
      }
      treeview?.expandNodes((node) => {
        return expandedIds.includes(node.id as number);
      })
    } else {
      viewPath = paths[id]
      fetchViewData(viewPath)
    }
  };
  import j from "jquery" ;
	import { onMount } from "svelte";
  onMount(() => {
    j('#tree-view')[0].children[1].classList.add('lexenddeca-normal-oslo-gray-20px')
  })
    
</script>

<div id="tree-view">
  <Tree
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
