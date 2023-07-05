<script lang="ts">

</script>

<div class="view-selection-frame">
  <div class="app-title">
    <h1 class="title valign-text-middle  lexenddeca-normal-geyser-24px-2">ENSEA Trendy Tables</h1>
    <div class="view-selection-separator"></div>
  </div>
  <div class="search-bar">
    <img class="vector-2" src="https://anima-uploads.s3.amazonaws.com/projects/63f7f6d546da9210f99dd5aa/releases/64a584ff82d80e5a118e543e/img/vector.svg" alt="Vector" />
    <div class="search valign-text-middle  lexenddeca-normal-oslo-gray-24px">Search</div>
  </div>
  <div class="view-tree-selector">
    <div class="left-buttons">
      <div class="view-sets">
        <div class="view-set-1 view-set">
          <img class="vector-3" src="https://anima-uploads.s3.amazonaws.com/projects/63f7f6d546da9210f99dd5aa/releases/64a584ff82d80e5a118e543e/img/vector-1.svg" alt="Vector" />
          <div class="view-set-1-1 valign-text-middle  ">View Set 1</div>
        </div>
        <div class="view-set-2 view-set">
          <img class="vector-4" src="https://anima-uploads.s3.amazonaws.com/projects/63f7f6d546da9210f99dd5aa/releases/64a584ff82d80e5a118e543e/img/vector-2.svg" alt="Vector" />
          <div class="view-set-2-1 valign-text-middle  lexenddeca-normal-oslo-gray-24px">View Set 2</div>
        </div>
        <div class="view-set-3 view-set">
          <img class="vector" src="https://anima-uploads.s3.amazonaws.com/projects/63f7f6d546da9210f99dd5aa/releases/64a584ff82d80e5a118e543e/img/vector-3.svg" alt="Vector" />
          <div class="view-set-3-1 valign-text-middle  lexenddeca-normal-oslo-gray-24px">View Set 3</div>
        </div>
        <div class="view-set-4 view-set">
          <img class="vector" src="https://anima-uploads.s3.amazonaws.com/projects/63f7f6d546da9210f99dd5aa/releases/64a584ff82d80e5a118e543e/img/vector-3.svg" alt="Vector" />
          <div class="view-set-4-1 valign-text-middle  lexenddeca-normal-oslo-gray-24px">View Set 4</div>
        </div>
      </div>
      <div class="settings">
        <div class="profile">
          <img class="vector-5" src="https://anima-uploads.s3.amazonaws.com/projects/63f7f6d546da9210f99dd5aa/releases/64a584ff82d80e5a118e543e/img/vector-5.svg" alt="Vector" />
          <div class="profile-1 valign-text-middle  lexenddeca-normal-oslo-gray-24px">Profile</div>
        </div>
        <div class="settings-1 settings-3">
          <img class="vector-6" src="https://anima-uploads.s3.amazonaws.com/projects/63f7f6d546da9210f99dd5aa/releases/64a584ff82d80e5a118e543e/img/vector-6.svg" alt="Vector" />
          <div class="settings-2 valign-text-middle  settings-3lexenddeca-normal-oslo-gray-24px">Settings</div>
        </div>
      </div>
      <div class="separator"></div>
    </div>
    <div class="tree">
      <div class="x-folded-1">
        <img class="vector-1" src="https://anima-uploads.s3.amazonaws.com/projects/63f7f6d546da9210f99dd5aa/releases/64a584ff82d80e5a118e543e/img/vector-7.svg" alt="Vector" />
        <div class="rectangle-32"></div>
      </div>
      <div class="x-folded-1">
        <img class="vector-7" src="https://anima-uploads.s3.amazonaws.com/projects/63f7f6d546da9210f99dd5aa/releases/64a584ff82d80e5a118e543e/img/vector-8.svg" alt="Vector" />
        <div class="rectangle-32-1 rectangle-32-3"></div>
        <div class="notes-tudiants valign-text-middle  lexenddeca-normal-oslo-gray-24px">Notes étudiants</div>
      </div>
      <div class="student-view">
        <img class="vector-1" src="https://anima-uploads.s3.amazonaws.com/projects/63f7f6d546da9210f99dd5aa/releases/64a584ff82d80e5a118e543e/img/vector-7.svg" alt="Vector" />
        <div class="rectangle-32-2 rectangle-32-3"></div>
        <div class="adresses-tudiants valign-text-middle  lexenddeca-normal-oslo-gray-24px">Adresses étudiants</div>
      </div>
      <div class="selected-item">
        <div class="rectangle-33"></div>
        <p class="vue-tudiants-1re-anne-adresses valign-text-middle  lexenddeca-normal-geyser-24px-2">Vue étudiants 1ère année adresses</p>
        <img class="vector-8" src="https://anima-uploads.s3.amazonaws.com/projects/63f7f6d546da9210f99dd5aa/releases/64a584ff82d80e5a118e543e/img/vector-10.svg" alt="Vector" />
      </div>
      <div class="item2"><p class="vue-tudiants-2me-anne-adresses valign-text-middle  lexenddeca-normal-oslo-gray-24px">Vue étudiants 2ème année adresses</p></div>
    </div>
  </div>
</div>

<style>
  .view-tree-selector {
    height: 940px;
    position: relative;
    display: flex;
    flex-direction: row;
    overflow: hidden;
    width: 1000px;
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
    width: 500px;
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
  .left-buttons {
    align-items: flex-start;
    display: flex;
    flex-direction: column;
    gap: 600px;
    justify-content: center;
    left: 0;
    position: absolute;
    top: 0;
    width: fit-content;
  }
  .view-selection-frame .view-set {
    align-items: center;
    display: flex;
    position: relative;
  }
  .vector {
    height: 25px;
    margin-left: -1.5px;
    min-width: 31px;
    position: relative;
  }
  .view-set-4-1 {
    letter-spacing: 0;
    line-height: normal;
    margin-top: -1px;
    position: relative;
    width: fit-content;
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
  .view-set-2-1 {
    letter-spacing: 0;
    line-height: normal;
    margin-top: -1px;
    position: relative;
    width: fit-content;
  }
  .vector-4 {
    height: 23px;
    margin-left: -1.5px;
    min-width: 28px;
    position: relative;
  }
  .view-set-3-1 {
    letter-spacing: 0;
    line-height: normal;
    margin-top: -1px;
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
  .view-selection-frame .settings-3 {
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
    height: 4px;
    left: -243px;
    position: absolute;
    top: 448px;
    transform: rotate(90deg);
    width: 900px;
  }
  .tree {
    align-items: flex-start;
    display: flex;
    flex-direction: column;
    gap: 1px;
    justify-content: center;
    left: 233px;
    position: absolute;
    top: 0;
    width: fit-content;
  }
  .selected-item {
    align-items: center;
    background-color: var(--shark);
    border: 1px solid;
    border-color: var(--bright-gray);
    display: flex;
    gap: 15px;
    justify-content: center;
    position: relative;
    width: fit-content;
  }
  .vector-8 {
    height: 29.57px;
    min-width: 36.56px;
    position: relative;
  }
  .rectangle-33 {
    background-color: var(--sea-green);
    height: 48px;
    min-width: 4px;
    position: relative;
    transform: rotate(180deg);
  }
  .vue-tudiants-1re-anne-adresses {
    height: 31px;
    letter-spacing: 0;
    line-height: normal;
    position: relative;
    width: 459px;
  }
  .x-folded-1 {
    align-items: center;
    display: flex;
    justify-content: center;
    position: relative;
    width: fit-content;
  }
  .rectangle-32 {
    background-color: var(--eerie-black);
    border-bottom-style: solid;
    border-bottom-width: 2px;
    border-color: var(--bright-gray);
    height: 50px;
    min-width: 625px;
    position: relative;
  }
  .vector-1 {
    height: 18.83px;
    min-width: 29.58px;
    position: relative;
  }
  .notes-tudiants {
    height: 31px;
    left: 40px;
    letter-spacing: 0;
    line-height: normal;
    position: absolute;
    top: 9px;
    width: 369px;
  }
  .vector-7 {
    height: 27.38px;
    min-width: 20.33px;
    position: relative;
  }
  .rectangle-32-1 {
    min-width: 605px;
  }
  .view-selection-frame .rectangle-32-3 {
    background-color: var(--eerie-black);
    border-bottom-style: solid;
    border-bottom-width: 2px;
    border-color: var(--bright-gray);
    height: 50px;
    position: relative;
  }
  .item2 {
    align-items: center;
    background-color: var(--eerie-black);
    border: 2px solid;
    border-color: var(--bright-gray);
    display: flex;
    gap: 10px;
    justify-content: center;
    padding: 10px 22px;
    position: relative;
    width: fit-content;
  }
  .vue-tudiants-2me-anne-adresses {
    height: 31px;
    letter-spacing: 0;
    line-height: normal;
    margin-top: -2px;
    position: relative;
    width: 443px;
  }
  .student-view {
    align-items: center;
    display: flex;
    gap: 15px;
    justify-content: center;
    position: relative;
    width: fit-content;
  }
  .rectangle-32-2 {
    min-width: 585px;
  }
  .adresses-tudiants {
    height: 31px;
    left: 45px;
    letter-spacing: 0;
    line-height: normal;
    position: absolute;
    top: 9px;
    width: 369px;
  }
</style>