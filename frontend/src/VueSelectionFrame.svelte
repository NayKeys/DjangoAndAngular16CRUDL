<script lang="ts">
	import { onMount } from 'svelte';
  import { writable } from 'svelte/store';
  import Tree from './VueTree.svelte';
  import type { ViewTree } from './requests';
  import { TextInputSkeleton, Search } from "carbon-components-svelte";
  import jquery from 'jquery';

  import type { Permissions } from './App.svelte';

  export let viewTree: ViewTree;
  export let fetchRequest: Function;
  export let buttonsShown: boolean = false;
  export let permissions: Permissions;

  let query: string = "";
  
  onMount(() => {
    jquery('.left-buttons').on('click', function() {
      buttonsShown = true
    })
    jquery(document).on('click', function(e) {
      if ((!jquery(e.target).hasClass('left-buttons')) && jquery(e.target).parents('.left-buttons').length == 0) { // if the target not a child of the left-buttons
        buttonsShown = false
      }
    })
  });
  const hideButtons = () => {
    buttonsShown = false
  }
  function performSearch(e) {
    query = e.originalTarget.value.toLowerCase();
  }
</script>


<div class="app-title">
  <h1 class="title valign-text-middle lexenddeca-normal-geyser-24px-2">ENSEA Trendy Tables</h1>
  <div class="view-selection-separator"></div>
</div>
<Search on:input={performSearch} placeholder="Search in tree..." autocomplete="on" autocorrect="off" />
<div class="view-tree-selector">
  <div class={"left-buttons-container "+(buttonsShown ? 'shown' : 'hidden')}>
    <div class="left-buttons" on:click={() => (buttonsShown = true)} on:keypress>
      <div class="view-sets">
        {#if viewTree}
          {#if viewTree.has_view_sets}
            {#each Object.keys(viewTree.root) as view_set_key}
              <div class="view-set">
                <img class="vector-3" src="https://anima-uploads.s3.amazonaws.com/projects/63f7f6d546da9210f99dd5aa/releases/64a584ff82d80e5a118e543e/img/vector-2.svg" alt="Vector" />
                <div class="view-set-1-1 valign-text-middle">{view_set_key}</div>
              </div>
            {/each}
          {:else}
            <div class="view-set">
              <img class="vector-3" src="https://anima-uploads.s3.amazonaws.com/projects/63f7f6d546da9210f99dd5aa/releases/64a584ff82d80e5a118e543e/img/vector-2.svg" alt="Vector" />
              <div class="view-set-1-1 valign-text-middle">Views</div>
            </div>
          {/if}
        {:else}
          {#each {length: 3} as _, i}
            <div class="view-set">
              <TextInputSkeleton hideLabel />
            </div>
          {/each}
        {/if}
      </div>
      <div class="settings">
        <div class="profile">
          <img class="vector-5" src="https://anima-uploads.s3.amazonaws.com/projects/63f7f6d546da9210f99dd5aa/releases/64a584ff82d80e5a118e543e/img/vector-5.svg" alt="Vector" />
          <div class="profile-1 valign-text-middle lexenddeca-normal-oslo-gray-24px">Profile</div>
        </div>
        <div class="settings-1 settings-3">
          <img class="vector-6" src="https://anima-uploads.s3.amazonaws.com/projects/63f7f6d546da9210f99dd5aa/releases/64a584ff82d80e5a118e543e/img/vector-6.svg" alt="Vector" />
          <div class="settings-2 valign-text-middle settings-3lexenddeca-normal-oslo-gray-24px">Settings</div>
        </div>
      </div>
    </div>
  </div>
  <div class="separator"></div>
  <div class="tree-container">
    {#if viewTree}
      {#key query}
        {#key viewTree}
          {#key permissions}
            {#if permissions}
              <Tree permissions={permissions} query={query} hideButtons={hideButtons} fetchRequest={fetchRequest} nodes={viewTree.root}/>
            {/if}
          {/key}
        {/key}
      {/key}
    {:else}
      <div class="tree">
        {#each {length: 10} as _, i}
          <TextInputSkeleton hideLabel />
        {/each}
      </div>
    {/if}
  </div>
</div>

<style>
  .hidden {
    width: 50px;
  }
  .shown {
    width: 300px;
  }
  .left-buttons-container {
    position: relative;
    transition: width 0.2s ease-in-out;
  }
  .view-tree-selector {
    position: relative;
    display: flex;
    gap: 5px;
    flex-direction: row;
    justify-content: start;
    overflow-y: scroll;
    width: fit-content;
    height: 100%;
  }
  .tree-container {
    position: relative;
    width: 500px;
    display: block;
    height: fit-content;
  }
  .tree {
    align-items: flex-start;
    display: flex;
    flex-direction: column;
    gap: 1px;
    justify-content: center;
    position: absolute;
    top: 0;
    overflow: hidden;
    width: 100%;
  }
  .view-tree-selector >*, .view-tree-selector >*>*, .view-tree-selector >*>*>*, .view-tree-selector >*>*>*>*, .view-tree-selector >*>*>*>*>* {
    overflow: hidden;
    white-space: nowrap;
  }
  .left-buttons {
    align-items: flex-start;
    display: flex;
    flex-direction: column;
    gap: 600px;
    justify-content: center;
    left: 0;
    position: absolute;
    top: 0;
    overflow: hidden;
    width: 100%;
  }
  .view-sets > *{
    width:100%;
    gap: 25px;
  }
  .view-sets {
    align-items: flex-start;
    display: flex;
    flex-direction: column;
    gap: 20px;
    position: relative;
    width: 100%;
  }

  .view-selection-separator {
    background-color: var(--bright-gray);
    border-radius: 10px;
    height: 4px;
    width: 100%;
    position: relative;
  }
  .search-bar {
    align-items: center;
    align-self: stretch;
    background-color: var(--shark);
    border-radius: 20px;
    display: flex;
    gap: 14px;
    padding: 12px 13px;
    position: relative;
  }
  .valign-text-middle {
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  .search {
    height: 30.61px;
    letter-spacing: 0;
    line-height: normal;
    margin-top: -1.8px;
    position: relative;
    width: 89.27px;
  }
  .vector-2 {
    height: 31px;
    min-width: 31px;
    position: relative;
  }
  .app-title {
    align-items: start;
    display: flex;
    flex-direction: column;
    gap: 5px;
    width: 100%;
    position: relative;
  }
  .title {
    height: 31px;
    letter-spacing: 0;
    line-height: normal;
    margin-top: -1px;
    position: relative;
  }
  .view-set {
    align-items: center;
    display: flex;
    position: relative;
  }
  .vector-3 {
    height: 43px;
    min-width: 43px;
    position: relative;
  }
  .view-set-1-1 {
    color: var(--sea-green);
    font-family: var(--font-family-lexend_deca);
    font-size: var(--font-size-l3);
    font-weight: 400;
    letter-spacing: 0;
    line-height: normal;
    position: relative;
    width: fit-content;
  }
  .settings {
    align-items: flex-start;
    display: flex;
    flex-direction: column;
    gap: 31px;
    height: 97px;
    position: relative;
    width: fit-content;
  }
  .profile {
    align-items: center;
    display: flex;
    gap: 19px;
    position: relative;
    width: fit-content;
  }
  .profile-1 {
    letter-spacing: 0;
    line-height: normal;
    position: relative;
    width: fit-content;
  }
  .vector-5 {
    height: 36px;
    min-width: 36px;
    position: relative;
  }
  .settings-1 {
    align-items: center;
    display: flex;
    gap: 22px;
  }
  .settings-3 {
    position: relative;
    width: fit-content;
  }
  .vector-6 {
    height: 18.9px;
    margin-left: -2px;
    min-width: 37.11px;
    position: relative;
  }
  .settings-2 {
    letter-spacing: 0;
    line-height: normal;
    margin-top: -1px;
  }
  .separator {
    background-color: var(--bright-gray);
    border-radius: 10px;
    width: 4px;
    height: 100%;
  }
</style>