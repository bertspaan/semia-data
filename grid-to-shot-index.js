#!/usr/bin/env node

const fs = require('fs')
const H = require('highland')
const R = require('ramda')

const GRID_FILE = process.argv[2]
const SHOTS_FILE = process.argv[3]

const csvStream = (filename) => H(fs.createReadStream(filename))
  .split()
  .compact()
  .map((line) => line.split(',').map(Number))

const grid = csvStream(GRID_FILE)
const shots = csvStream(SHOTS_FILE)

function loadGrid () {
  return new Promise((resolve) => {
    grid
      .map(([x, y]) => ({x, y}))
      .toArray((grid) => resolve(grid))
  })
}

function loadShots () {
  return new Promise((resolve) => {
    shots
      .map(([videoId, shotId]) => ({videoId, shotId}))
      .toArray((shots) => resolve(shots))
  })
}

async function run () {
  const grid = await loadGrid()
  const shots = await loadShots()

  const sortByX = R.sortBy(R.prop('y'))

  const shotsGrid = Object.values(
    R.groupBy(
      R.prop('x'), shots.map((shot, index) => {
        const str = `${shot.videoId}_${shot.shotId}`
        return {
          ...grid[index],
          str
        }
      })
    )
  ).map((row) => sortByX(row).map(R.prop('str')))

  console.log(JSON.stringify(shotsGrid))
}

run()
