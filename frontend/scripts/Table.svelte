<script lang="ts">
  
</script>

<div class="table-frame screen">
  <div class="frame-31">
    <h1 class="vue-tudiants-1re-anne valign-text-middle">Vue étudiants 1ère année</h1>
    <div class="top-seperator"></div>
  </div>
  <div class="table-buttons">
    <div class="search">
      <img class="vector" src="https://anima-uploads.s3.amazonaws.com/projects/63f7f6d546da9210f99dd5aa/releases/64a3f5479ef0ce55861f0160/img/vector.svg" alt="Vector" />
      <div class="search-1 valign-text-middle lexenddeca-normal-oslo-gray-24px">Search</div>
    </div>
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
  <div class="table">
    <article class="row">
      <div class="cell">
        <div class="content"><div class="text lexenddeca-semi-bold-oslo-gray-20px  ">First Name</div></div>
      </div>
      <div class="cell-1 cell-8">
        <div class="content"><div class="text lexenddeca-semi-bold-oslo-gray-20px  ">Last Name</div></div>
      </div>
      <div class="cell-2 cell-8">
        <div class="content"><div class="text lexenddeca-semi-bold-oslo-gray-20px  ">email</div></div>
      </div>
      <div class="cell-3 cell-8">
        <div class="content"><div class="text lexenddeca-semi-bold-oslo-gray-20px  ">Address</div></div>
      </div>
    </article>
    <article class="row-1">
      <div class="cell-4cell-8">
        <div class="content"><div class=" text-1  lexenddeca-normal-geyser-24px">Yan</div></div>
      </div>
      <div class="cell-5 cell-8">
        <div class="content"><div class=" text-1  lexenddeca-normal-geyser-24px">Regojo</div></div>
      </div>
      <div class="cell-6 cell-8">
        <div class="content"><div class=" text-1  lexenddeca-normal-geyser-24px">yan.regojo@ensea.fr</div></div>
      </div>
      <div class="cell-7 cell-8">
        <div class="content"><p class=" text-1  lexenddeca-normal-geyser-24px">21 rue de la Bassée Sain</p></div>
      </div>
    </article>
  </div>
</div>

<style>
  /* Variables */
  :root {
    --black: rgba(0, 0, 0, 1);
    --eerie-black: rgba(20, 24, 27, 1);
    --shark: rgba(30, 36, 41, 1);
    --bright-gray: rgba(54, 64, 73, 1);
    --masala: rgba(66, 59, 59, 1);
    --oslo-gray: rgba(138, 144, 151, 1);
    --silver: rgba(210, 197, 198, 1);
    --geyser: rgba(215, 221, 231, 1);
    --dawn-pink: rgba(241, 232, 232, 1);
    --white: rgba(255, 255, 255, 1);
    --font-size-xs: 40px;
    --font-size-m3: 20px;
    --font-size-l3: 24px;
    --font-size-s2: 48px;
    --font-size-m2: 64px;
    --font-size-l2: 80px;
    --font-size-xl2: 110px;
    --font-family-inter: "Inter";
    --font-family-lexend_deca: "Lexend Deca";
    --font-family-lexend_deca-medium: "Lexend Deca-Medium";
    --font-family-nats-regular: "NATS-Regular";
  } /* Classes */
  .lexenddeca-normal-oslo-gray-24px {
    color: var(--oslo-gray);
    font-family: var(--font-family-lexend_deca);
    font-size: var(--font-size-l3);
    font-weight: 400;
    font-style: normal;
  }
  .lexenddeca-normal-geyser-24px {
    color: var(--geyser);
    font-family: var(--font-family-lexend_deca);
    font-size: var(--font-size-l3);
    font-weight: 400;
    font-style: normal;
  }
  .lexenddeca-semi-bold-oslo-gray-20px {
    color: var(--oslo-gray);
    font-family: var(--font-family-lexend_deca);
    font-size: var(--font-size-m3);
    font-weight: 600;
    font-style: normal;
  }

  @import url("https://fonts.googleapis.com/css?family=Lexend+Deca:400,600");
  .table-frame {
    align-items: flex-start;
    background-color: var(--shark);
    border: 1px none;
    display: flex;
    flex-direction: column;
    gap: 50px;
    justify-content: center;
    min-width: 1164.44px;
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
  .search {
    align-items: center;
    background-color: var(--eerie-black);
    border: 2px solid;
    border-color: var(--bright-gray);
    border-radius: 5px;
    display: flex;
    gap: 12px;
    padding: 12px 15px;
    position: relative;
    width: 748px;
  }
  .vector {
    height: 31px;
    min-width: 31px;
    position: relative;
  }
  .search-1 {
    height: 30.61px;
    letter-spacing: 0;
    line-height: normal;
    margin-top: -1.8px;
    position: relative;
    width: 89.27px;
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
  .table {
    align-items: flex-start;
    align-self: stretch;
    border-radius: 4px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    position: relative;
  }
  .row-1 {
    align-items: flex-start;
    align-self: stretch;
    background-color: #ffffff00;
    display: flex;
    height: 51px;
    overflow: hidden;
    position: relative;
  }
  .table-frame .cell-8 {
    align-items: flex-start;
    align-self: stretch;
    background-color: var(--shark);
    border-color: var(--bright-gray);
    display: flex;
    flex-direction: column;
    position: relative;
  }
  .cell-4 {
    border-top-style: solid;
    border-top-width: 1px;
    width: 250px;
  }
  .content {
    align-items: flex-start;
    align-self: stretch;
    display: flex;
    padding: 10px 12px;
    position: relative;
  }
  .text-1 {
    flex: 1;
    letter-spacing: 0;
    line-height: 31.2px;
    margin-top: -1px;
    position: relative;
    white-space: nowrap;
  }
  .cell-5 {
    border-left-style: solid;
    border-left-width: 1px;
    border-top-style: solid;
    border-top-width: 1px;
    width: 250px;
  }
  .cell-7 {
    border-left-style: solid;
    border-left-width: 1px;
    border-top-style: solid;
    border-top-width: 1px;
    width: 320px;
  }
  .cell-6 {
    border-left-style: solid;
    border-left-width: 1px;
    border-top-style: solid;
    border-top-width: 1px;
    width: 300px;
  }
  .row {
    align-items: flex-start;
    align-self: stretch;
    background-color: #ffffff00;
    display: flex;
    height: 46px;
    overflow: hidden;
    position: relative;
  }
  .cell {
    align-items: flex-start;
    align-self: stretch;
    background-color: var(--shark);
    border: 0px none;
    display: flex;
    flex-direction: column;
    position: relative;
    width: 250px;
  }
  .text {
    flex: 1;
    letter-spacing: 0;
    line-height: 26px;
    margin-top: -1px;
    position: relative;
    white-space: nowrap;
  }
  .cell-1 {
    border-left-style: solid;
    border-left-width: 1px;
    width: 250px;
  }
  .cell-3 {
    border-left-style: solid;
    border-left-width: 1px;
    width: 320px;
  }
  .cell-2 {
    border-left-style: solid;
    border-left-width: 1px;
    width: 300px;
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
    width: 394px;
  }
  .top-seperator {
    background-color: var(--bright-gray);
    border-radius: 10px;
    height: 4px;
    min-width: 1114px;
    position: relative;
  }
</style>