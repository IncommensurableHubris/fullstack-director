# PlantPal — Product Brief

PlantPal is a watering reminder for people who keep houseplants and keep killing them. A user adds each plant
once, PlantPal works out when it needs water, and it nags — reliably, on-device — until the user taps "watered."
The brief below is final; build against it as written.

## What it does

A user adds a plant by name and gives it a watering interval (every plant is different — a cactus is not a fern).
PlantPal schedules a reminder notification for each plant on that interval and keeps rescheduling from the last
time the user marked it watered. Tapping "watered" resets the clock; nothing else does.

Reminders fire as local notifications on the device — PlantPal does not depend on a server being reachable for a
reminder to go off on time. If today isn't a good day for a particular plant, the user can snooze that one
reminder without disturbing any other plant's schedule.

## Scope

v1 is a single person's plant list on one device. No shared households, no plant-care social feed, no plant-ID
camera, no marketplace. A user who wants those can wait for a later release; v1 ships the reminder loop and
nothing else.
