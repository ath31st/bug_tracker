<!-- src/views/AboutView.vue -->
<template>
  <v-container class="about-container">
    <v-row justify="center">
      <v-col cols="8">
        <v-card class="pa-6">
          <v-card-title class="text-h4 font-weight-bold primary--text">
            <v-icon left large>mdi-bug</v-icon>
            О проекте: Bug Tracker
          </v-card-title>
          <v-card-subtitle class="text-h6 mt-2">
            Простое приложение для фиксации и отслеживания багов
          </v-card-subtitle>
          <v-divider class="my-4"></v-divider>
          <v-card-text>
            <p>
              Это минималистичный баг-трекер, созданный для заведения задач и
              контроля процесса исправления багов(ошибок). Он разработан с
              использованием современных технологий, что делает его легким и
              простым в использовании.
            </p>
            <p>
              Проект фокусируется на минимализме и удобстве интерфейса,
              предоставляя пользователям необходимые инструменты для управления
              задачами.
            </p>
            <v-list dense>
              <v-list-item>
                <v-list-item-title class="font-weight-medium">
                  Технологии:
                </v-list-item-title>
                <v-list-item-subtitle>
                  <v-row>
                    <v-col cols="6">
                      <strong>Frontend:</strong>
                      <ul>
                        <li>Vue 3</li>
                        <li>Pinia (состояние)</li>
                        <li>Vuetify (UI)</li>
                        <li>TypeScript</li>
                        <li>Vite (сборка)</li>
                        <li>Vue Router (маршрутизация)</li>
                      </ul>
                    </v-col>
                    <v-col cols="6">
                      <strong>Backend:</strong>
                      <ul>
                        <li>Flask (веб-фреймворк)</li>
                        <li>SQLAlchemy (ORM)</li>
                        <li>Flask-JWT-Extended (авторизация)</li>
                        <li>PostgreSQL (БД)</li>
                        <li>Marshmallow (валидация данных)</li>
                        <li>Alembic (миграции БД)</li>
                      </ul>
                    </v-col>
                  </v-row>
                </v-list-item-subtitle>
              </v-list-item>
              <v-list-item>
                <v-list-item-title>Дата выполнения проекта:</v-list-item-title>
                <v-list-item-subtitle>Март 2025</v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts"></script>

<style scoped>
ul {
  padding-left: 20px;
  margin-top: 4px;
}
</style>
