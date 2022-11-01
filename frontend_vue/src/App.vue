<template>
  <div class="wrapper">
    <!-- Nav -->
    <nav class="navbar is-dark" role="navigation" aria-label="main navigation">
      <div class="navbar-brand">
        <router-link :to="{name: 'Home'}" class="navbar-item">
          <strong>WhereIs</strong>
        </router-link>

        <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>

      <div id="navbarBasicExample" class="navbar-menu">
        <div class="navbar-start">
          <router-link :to="{name: 'Home'}" class="navbar-item">
            Home
          </router-link>

          <router-link :to="{name: 'LocationForm'}" class="navbar-item">
            Location Form
          </router-link>

          <router-link :to="{name: 'LocationGrid'}" class="navbar-item">
            Location Grid
          </router-link>
        </div>

        <div class="navbar-end">
          <div class="navbar-item">
            <div class="buttons">
              <a class="button is-primary">
                <strong>Sign up</strong>
              </a>
              <a class="button is-light">
                Log in
              </a>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <router-view/>

    <!-- Footer -->
    <footer class="footer mt-6">
      <div class="content has-text-centered">
        Copyright (c) 2022
      </div>
    </footer>
  </div>
</template>

<style lang="scss">
@import '../node_modules/bulma'
</style>
