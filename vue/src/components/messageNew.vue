<template>
  <div class="column is-10 is-offset-1">
    <div class="box">
      <article class="media">
        <div class="media-content">
          <div class="content">
            <div class="field has-addons has-addons-centered">
              <div class="control is-expanded">
                <input class="input" type="text" v-model="message" placeholder="Add new message" />
              </div>
              <div class="control">
                <button class="button is-link" v-on:click="submit">Add</button>
              </div>
            </div>
          </div>
        </div>
      </article>
    </div>
  </div>
</template>

<script>
export default {
  name: "newMessage",
  data() {
    return {
      message: null
    };
  },
  methods: {
    submit() {
      this.$store.dispatch("messageAdd", this.message);
      this.message = null;
    }
  }
};
</script>
