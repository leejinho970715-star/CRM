(() => {
  const {groups,examples,render} = window.CRMStatus;
  document.getElementById('status-groups').innerHTML = groups.map(group => `<article class="tone-card"><small>${group.color}</small><h2>${group.name}</h2><p>${group.description}</p><div class="tone-examples">${group.examples.map(value=>render(value)).join('')}</div><div class="tone-colors">텍스트 ${group.fg} · 배경 ${group.bg}</div></article>`).join('');
  document.getElementById('status-examples').innerHTML = examples.map(row => `<div class="mapping-row"><h3>${row.name}</h3><div class="mapping-labels">${row.values.map(value=>render(value,row.context)).join('')}</div></div>`).join('');
})();
