import Vue from 'vue'
import Vuex from 'vuex'
import axios from "axios";

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    jwt: '',
    messages: [],
    userCache: {},
    
  },
  mutations: {
    JWT_SET(state, jwt) {
      state.jwt = jwt;
    },
    MESSAGES_UPDATE(state, messages) {
      state.messages = messages;
    },
    USER_CACHE_UPDATE(state, users) {
      state.userCache = users;
    },
  },
  actions: {
    jwtSet({commit}, jwt) {
      axios.defaults.headers.common['Authorization'] = jwt;
      commit('JWT_SET', jwt);
    },
    messageGet({getters, dispatch, commit}) {
      axios.get("/messages/").then(function(response) {
        if (response.data) {
          let x;
          for (x of response.data){
            if (!getters.userCache[x.user_id]) {
              // TODO: This is async, so repeated messages will be fetched multiple times
              dispatch('userCacheLookup', x.user_id);
            }
          }
          commit('MESSAGES_UPDATE', response.data);
        }
      });
    },
    messageAdd({dispatch}, text) {
      axios.post('/messages/add', {text}).then(function() {
        dispatch('messageGet');
      });
    },
    userCacheLookup({dispatch}, userId) {
      axios.get("/login/lookup", {params: {id: userId} }).then(function(response) {
        let user = {}
        user[userId] = response.data
        dispatch('userCacheAdd', user);
      });
    },
    userCacheAdd({commit, getters}, user) {
      commit('USER_CACHE_UPDATE', {...getters.userCache, ...user});
    },
  },
  getters: {
    jwt: state => state.jwt,
    messages: state => state.messages,
    userCache: state => state.userCache,
  }
})
