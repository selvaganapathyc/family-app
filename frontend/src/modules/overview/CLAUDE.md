# Overview Module (Frontend)

## Purpose
Home screen shown after login. Aggregates data across all modules in one view — urgent alerts, recent activity, and a snapshot card per module.

## Routes
| Path | View | Description |
|---|---|---|
| `/overview` | `OverviewView.vue` | Main overview screen |

Default redirect from `/` goes here. After login, users land here.

## File Structure
```
modules/overview/
├── views/
│   └── OverviewView.vue          # Main view — greeting, top grid, module snapshots
├── components/
│   ├── AlertsPanel.vue           # Urgent items (budget exceeded, etc.)
│   ├── ActivityFeed.vue          # Recent transactions across all members
│   └── ModuleSnapshot.vue        # Reusable summary card per module
├── services/
│   └── overview.service.js       # GET /overview/summary
└── router/
    └── overview.routes.js
```

## Data Flow
`OverviewView.vue` → `overview.service.js` → `GET /overview/summary` → backend aggregation

Response shape:
```js
{
  alerts: [{ id, message, module, icon, severity: 'warning'|'danger'|'info' }],
  recentActivity: [{ id, member, memberInitial, action, amount, type, module, timeAgo }],
  finance: { totalIncome, totalExpenses, netBalance }
}
```

## AlertsPanel Severity Styles
| Severity | Color | Use for |
|---|---|---|
| `warning` | Yellow | Budget 80–99% used |
| `danger` | Red | Budget exceeded (100%+) |
| `info` | Blue | Informational alerts |

## Adding a New Module Snapshot
In `OverviewView.vue`, add a `<ModuleSnapshot>` component:
```vue
<ModuleSnapshot icon="❤️" label="Health" route="/health/dashboard">
  <!-- slot content: stats go here -->
</ModuleSnapshot>
```
Remove `coming-soon` prop once the module is live.

## Sidebar Behavior
Overview has no sidebar. When `activeModule === 'overview'`, `AppSidebar.vue` renders nothing (hidden automatically — `MODULE_NAV.overview` is an empty array).
