<template>
  <div class="home">
    <MessageNew v-if="jwt" />
    <Message v-for="message in messages" v-bind:key="message.id" v-bind:message="message" />
  </div>
</template>

<script>
import MessageNew from "@/components/messageNew";
import Message from "@/components/message";
import { mapGetters } from "vuex";

export default {
  name: "home",
  data() {
    return {
      todo: ""
    };
  },
  computed: {
    ...mapGetters([
      "isConnected",
      "name",
      "email",
      "picture",
      "personalID",
      "jwt",
      "messages",
      "userCache",
    ])
  },
  components: {
    MessageNew, Message
  },
  mounted() {
    this.$store.dispatch("messageGet");
  },
};
</script>
