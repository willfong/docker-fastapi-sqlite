<template>
  <div class="column is-8 is-offset-2">
    <div class="card">
      <div class="card-content">
        <h3 class="title is-3">“{{message.message_text}}”</h3>
        <p class="subtitle">{{username}}</p>
      </div>
      <footer class="card-footer">
        <p class="card-footer-item">
          <span>
            {{fmtDate}}
          </span>
        </p>
        <p class="card-footer-item">
          <span>
            .
          </span>
        </p>
      </footer>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import moment from 'moment/moment';

export default {
  name: "Message",
  props: ["message"],
  computed: {
    ...mapGetters(["userCache"]),
    username: function () {
      if (this.userCache[this.message.user_id]) {
        return this.userCache[this.message.user_id]['name'];
      } else {
        return '';
      }
    },
    fmtDate: function() {
      return moment.utc(this.message.datetime).fromNow();
    }
  },
};
</script>
