<script lang="ts">
  import { TreeView as Tree} from "carbon-components-svelte";
  import type { ViewTree, View, TreeNode, ViewList } from "./requests";
  import j from "jquery" ;
  import { onMount } from "svelte";

  export let nodes: TreeNode<View>;
  export let fetchViewData: Function;
  export let hideButtons: Function;
  export let query: string;
    
  let viewPath: string;
  let treeview: Tree;
  let activeId = "";
  let selectedIds = [];
  let expandedIds = [1, 2, 14];
  let selectedItemId
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
      if (query.length > 0) {
        if (name == query || name.toLowerCase().includes(query)) {
          selectedItemId = i;
          return {id: i++, text: name}
        } else {
          return null;
        }
      } else {
        return {id: i++, text: name}
      }
    }
    else {
      let childrenOfNode = []
      for (let [key, value] of Object.entries(node)) {
        let child = exploreTree(value, key)
        if (child != null)
          childrenOfNode.push(child)
      }
      if (name == query || name.toLowerCase().includes(query)) {
        selectedIds.push(i)
        expandedIds.push(i)
      }
      if (query.length > 0)
        if (childrenOfNode.length == 0)
          return null;
      return {id: 100+(i++), text: name, children: childrenOfNode}
    }
  }
  
  for (let [key, value] of Object.entries(nodes)) {
    const node = exploreTree(value, key);
    if (node != null)
      children.push(node)
  }
  // Parent node with children has id >= 100

  if (selectedItemId) {
    for (let id in selectedIds) {
      if (selectedIds[id] == selectedItemId) {
        selectItem(id, false)
        break
      }
    }
    selectItem(selectedItemId, false)
  }
  
  function selectItem(id: any, fetch: boolean = true) {
    hideButtons()  // This component has a stopPropagation on click, so we need to fire this function that way
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
      if (fetch)
        fetchViewData(viewPath)
    }
  };

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
    on:select={({ detail }) => selectItem(detail.id)}
  />
</div>

<style>
  div {
    margin-top: var(--cds-spacing-05);
  }
</style>
