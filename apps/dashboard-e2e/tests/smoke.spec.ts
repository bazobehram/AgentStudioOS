import { test, expect } from '@playwright/test';

const API = 'http://localhost:8001';

async function getAgents(){
  const r = await fetch(`${API}/agents`);
  return await r.json();
}

test('dashboard smoke: create agent, draft_post, approve post_x', async ({ page }) => {
  await page.goto('http://localhost:4200');
  await page.getByText('Agents').click();
  await page.locator('input[name="name"]').fill('Agent A');
  await page.getByRole('button', { name: 'Create' }).click();

  const agents = await getAgents();
  const agentId = agents[0].id;

  await page.getByText('Tasks').click();
  await page.locator('input[name="agent_id"]').fill(agentId);
  await page.locator('select[name="type"]').selectOption('draft_post');
  await page.getByRole('button', { name: 'Enqueue' }).click();

  await page.locator('select[name="type"]').selectOption('post_x');
  await page.locator('input[name="payload"]').fill('{"text":"hello"}');
  await page.getByRole('button', { name: 'Enqueue' }).click();

  await page.getByText('Approvals').click();
  await page.waitForTimeout(1000);
  const approve = page.getByRole('button', { name: 'Approve' });
  if (await approve.count() > 0) { await approve.first().click(); }

  await page.getByText('Logs').click();
  await page.locator('#logTaskId').fill(agentId);
  await page.getByText('Load').click();
  await expect(page.locator('#logContent')).toBeVisible();
});
